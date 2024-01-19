from django.db.models import Q, F
from django.utils import timezone
from django.utils.timezone import now

from firebase.authentication import FirebaseAuthentication
from firebase_admin import firestore

from mota.serializers.rooms import *
from mota.serializers.users import *

from mota.models.rooms import Rooms
from mota.models.users_rooms import UsersRooms
from mota.models.chats import Chats
from mota.models.notices import Notices

from mota.utils import load_user, send_fcm_notification

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from swagger.views import rooms_get, rooms_post, rooms_id_get, rooms_id_put, rooms_id_delete, rooms_me_get, rooms_id_terminate_put, rooms_me_all_get
import sys

db = firestore.client()

def getMember(roomId):
    members = UsersRooms.objects.filter(room_id=roomId, deleted_at__isnull=True)
    membersId = members.values_list('user_id', flat=True)
    membersInfo = Users.objects.filter(uid__in=membersId)
    serializer = UsersGetSerializer(membersInfo, many=True)
    
    return serializer.data


# @ /api/rooms : GET POST
# @ # 방 전체 조회 및 생성
class RoomsAPI(APIView):
    firebase = FirebaseAuthentication()
    post_key = ["price", "party_limit", "locate_start", "locate_end", "plan_at", "content", "option"]

    # * GET /api/rooms
    # * 현재 이용가능한 방 전부 조회 
    @swagger_auto_schema(**rooms_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)

        ten_minutes_after = now() - timedelta(minutes=10)
        
        rooms = Rooms.objects.filter(~Q(user_id=user.uid) & 
                                     Q(party_now__lt=F('party_limit')) & 
                                     Q(plan_at__gte=ten_minutes_after) & 
                                     Q(is_end=False) &
                                     Q(deleted_at__isnull=True)) 
        
        serializer = RoomsGetSerializer(rooms, many=True)
        
        for data in serializer.data:
            data.update({'members' : getMember(data["id"])})
            
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
    
    # TODO : 법에 따른 생성 시간 제한
    # * POST /api/rooms
    # * 방 생성 
    @swagger_auto_schema(**rooms_post)
    def post(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        
        # 모든 필요 값이 request.data에 없을 경우 
        if not all(key in request.data for key in self.post_key):
            return Response(data={"ERROR" : "잘못된 요청 전송됨"},
                                  status=status.HTTP_400_BAD_REQUEST)
        
        # 날자 값이 올바른 형식을 가졌는지 확인 
        try:
            time = datetime.strptime(request.data["plan_at"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                time = datetime.strptime(request.data["plan_at"], "%Y-%m-%dT%H:%M:%S")
            except ValueError:     
                return Response(data={"ERROR" : "요청이 잘못된 형식을 가짐"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if time <= datetime.now():
            return Response(data={"ERROR" : "일정이 현재보다 과거임"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 방 생성
        myRoom = Rooms.objects.create(user_id=user.uid, 
                             price=request.data["price"],
                             party_limit=request.data["party_limit"],
                             locate_start=request.data["locate_start"],
                             locate_end = request.data["locate_end"],
                             plan_at=time,
                             content = request.data["content"],
                             option = request.data["option"])
        
        # 채팅방 생성 
        myChat = Chats.objects.create(chat_name=f"{user.nickname}님의 카풀", user=user)
        
        dbInfo_ref = db.collection('chat_info').document(str(myChat.chat_uuid))
        dbInfo_obj = {
            "room_id": myRoom.pk,
            "members" : [str(user.uid)],
            "chat_count": 0,
            "last_chat": "",
            "is_end": False,
            "created_at": timezone.now(),
            "updated_at": timezone.now()
        }
        dbInfo_ref.set(dbInfo_obj)
        
        dbData_ref = db.collection('chat_data').document(str(myChat.chat_uuid))
        dbData_obj = {
            "messages": []
        }
        dbData_ref.set(dbData_obj)
        
        return Response(status=status.HTTP_201_CREATED)
        
        
# @ /api/rooms/{id} : GET PUT DELETE
# @ # 특정 방 조회 및 생성
class RoomByIdAPI(APIView):   
    # * GET /api/rooms/{roomId}
    # * 특정 방 조회
    @swagger_auto_schema(**rooms_id_get)
    def get(self, request, roomId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)

        try:
            rooms = Rooms.objects.get(id=roomId, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "방 탐색 실패"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        serializer = RoomsGetSerializer(rooms, many=False)
        data = dict(serializer.data)
        data['members'] = getMember(serializer.data["id"])
        
        return Response(data=data,
                        status=status.HTTP_200_OK)
    
    # * PUT /api/rooms/{roomId}
    # * 방 정보 수정 
    @swagger_auto_schema(**rooms_id_put)
    def put(self, request, roomId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 날자 값이 올바른 형식을 가졌는지 확인
        if "plan_at" in request.data:
            try:
                time = datetime.strptime(request.data["plan_at"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return Response(data={"ERROR" : "잘못된 날짜 형식"},
                                status=status.HTTP_400_BAD_REQUEST)
            # 현재 날짜보다 후인 경우만
            if time < datetime.now():
                return Response(data={"ERROR" : "설정한 날짜 값이 과거에 속함"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        # 내 방이 아닐경우 에러
        try:
            room = Rooms.objects.get(id=roomId, user_id=user.uid, is_end=False, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "방에 대한 권한이 없음"},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        if "price" in request.data: 
            room.price = request.data["price"]
        if "party_limit" in request.data:
            room.party_limit = request.data["party_limit"]
        if "locate_start" in request.data:
            room.locate_start = request.data["locate_start"]
        if "locate_end" in request.data:
            room.locate_end = request.data["locate_end"]
        if "plan_at" in request.data:
            room.plan_at = request.data["plan_at"]
        if "content" in request.data:
            room.content = request.data["content"]
        if "option" in request.data:
            room.option = request.data["option"]
        room.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # * DELETE /api/rooms/{roomId}
    # * 방 정보 삭제  
    @swagger_auto_schema(**rooms_id_delete)
    def delete(self, request, roomId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 내 방이 아닐경우 에러
        try:
            room = Rooms.objects.get(id=roomId, user_id=user.uid, is_end=False, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "조건을 만족하는 방 없음"},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        room.deleted_at = datetime.now()
        room.save()
        
        # 알림 전송 
        members = UsersRooms.objects.filter(room_id=roomId, deleted_at__isnull=True).values_list('user', flat=True)
        for member in members:
            Notices.objects.create(user=member, 
                               message={
                                    "type" : "roomCancel",
                                    "roomId" : roomId,
                                    "message" : f"{room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀을 취소하였습니다."}
                               )
            send_fcm_notification(
                user=member,
                title="카풀 일정 취소",
                body=f"{room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀을 취소하였습니다."
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)


# @ /api/rooms/{id}/terminate : PUT
# @ # 특정 방 종료 설정
class RoomByIdTerminateAPI(APIView):
    # * PUT /api/rooms/{roomId}/terminate
    # * 특정 방 운행 종료
    @swagger_auto_schema(**rooms_id_terminate_put)
    def put(self, request, roomId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)

        try:
            room = Rooms.objects.get(id=roomId, 
                                    user_id=user.uid,
                                    is_end=False,
                                    deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "방 탐색 실패"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        room.is_end = True
    
        room.save()
        
        # 알림 전송 : 방장
        Notices.objects.create(user_id=room.user.uid, 
                               message={
                                    "type" : "myRoomEnd",
                                    "roomId" : room.pk,
                                    "message" : f"{room.user.nickname} 님의 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 진행되는 카풀이 종료되었습니다.",
                                    "url" : "https://docs.google.com/forms/d/e/1FAIpQLScTwqda5ffvsimCm8DpxLNRZL-ipBwgn1aTrtHSVCXL3l6zwg/viewform?usp=sf_link"}
                               )
        send_fcm_notification(
            user=room.user,
            title="카풀 종료",
            body=f"{room.user.nickname} 님의 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 진행되는 카풀이 종료되었습니다."
        )
        
        # 알림 전송 : 유저 
        members = UsersRooms.objects.filter(room_id=room.pk, deleted_at__isnull=True)
        for member in members:
            Notices.objects.create(user_id=member.user.uid,
                               message={
                                    "type" : "roomEnd",
                                    "roomId" : room.pk,
                                    "message" : f"{room.user.nickname} 님의 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 진행되는 카풀이 종료되었습니다.",
                                    "url" : "https://docs.google.com/forms/d/e/1FAIpQLScTwqda5ffvsimCm8DpxLNRZL-ipBwgn1aTrtHSVCXL3l6zwg/viewform?usp=sf_link"}
                               )
            send_fcm_notification(
                user=member.user,
                title="카풀 종료",
                body=f"{room.user.nickname} 님의 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 진행되는 카풀이 종료되었습니다."
            )

        # 채팅방 검색
        roomChats = Chats.objects.filter(user=room.user)
        if roomChats.count() <= 0:
            return Response(data={"ERROR" : "채팅방이 존재하지 않음"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        myChat = None
        myDB = None
        for roomChat in roomChats:
            db_ref = db.collection('chat_info').document(str(roomChat.chat_uuid))
            try:
                db_data = db_ref.get()
            except:
                continue
            if not db_data.exists:
                continue
            
            dict = db_data.to_dict()
            if dict["room_id"] == room.pk:
                myChat = roomChat
                myDB = db_ref
                break
        
        if myChat is None or myDB is None:
            return Response(data={"ERROR" : "채팅방이 존재하지 않음"}, 
                            status = status.HTTP_404_NOT_FOUND)
            
        myDB.update({
            "is_end": True
        })
        
        return Response(status=status.HTTP_200_OK)

# @ /api/rooms/me : GET
# @ # 내가 생성한 방 조회
class RoomsByMeAPI(APIView):
    # * GET /api/rooms/me
    # * 내가 생성한 방 전부 조회 
    @swagger_auto_schema(**rooms_me_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)

        # all, host, member
        participateRoom = UsersRooms.objects.filter(user_id=user.uid, 
                                                    deleted_at__isnull=True).values_list('room_id')
        rooms = Rooms.objects.filter((Q(user_id=user.uid) | Q(id__in=participateRoom)) & 
                                     Q(is_end=False) &
                                     Q(deleted_at__isnull=True)
                                     ).order_by('plan_at')
        
        serializer = RoomsGetSerializer(rooms, many=True)
        
        for data in serializer.data:
            if data["user"]["uid"] == str(user.uid):
                data["type"] = "host"
            else:
                data["type"] = "member"
            data.update({'members' : getMember(data["id"])})
        
        
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

# @ /api/rooms/me/all : GET
# @ # 내가 생성한 모든 방 조회
class RoomsByMeAllAPI(APIView):
    # * GET /api/rooms/me/all
    # * 종료와 상관없이
    @swagger_auto_schema(**rooms_me_all_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)

        # all, host, member
        participateRoom = UsersRooms.objects.filter(user_id=user.uid).values_list('room_id')
        rooms = Rooms.objects.filter((Q(user_id=user.uid) or Q(id__in=participateRoom))& 
                                     Q(deleted_at__isnull=True)
                                     ).order_by('plan_at')
        
        serializer = RoomsGetSerializer(rooms, many=True)
        
        for data in serializer.data:
            if data["user"]["uid"] == str(user.uid):
                data["type"] = "host"
            else:
                data["type"] = "member"
            data.update({'members' : getMember(data["id"])})
        
        
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

'''
rooms POST
{
    "price": 1000,
    "party_limit": 4,
    "locate_start": "사당역",
    "locate_end": "남대문역",
    "plan_at": "2023-08-17 16:10:00"
    "content": "오실분 구해요~",
    "option": {
        "age": "anybody",
        "gender": "anybody"
    },
}
'''

