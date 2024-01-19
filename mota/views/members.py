from firebase_admin import firestore
from google.cloud.firestore import ArrayRemove

from mota.serializers.members import *
from mota.serializers.users import *

from mota.models.rooms import Rooms
from mota.models.notices import Notices
from mota.models.users_rooms import UsersRooms
from mota.models.users import Users
from mota.models.chats import Chats

from mota.utils import send_fcm_notification, load_user

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from swagger.views import rooms_id_member_get, rooms_id_member_me_delete, rooms_id_member_id_delete

db = firestore.client()


# @ /api/rooms/{roomId}/member : GET POST
# @ 현재 방의 인원 확인 
class MembersAPI(APIView):  
    # * GET /api/rooms/{roomId}/member
    # * 현재 방의 모든 인원 조회
    @swagger_auto_schema(**rooms_id_member_get)
    def get(self, request, roomId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 입력된 방을 가진 모든 유저 조회
        members = UsersRooms.objects.filter(room_id=roomId, deleted_at__isnull=True)
        
        membersId = members.values_list('user_id', flat=True)
        membersInfo = Users.objects.filter(uid__in=membersId)
        
        serializer = UsersGetSerializer(membersInfo, many=True)
        #serializer = MembersGetSerializer(members, many=True)
        if not serializer:
            return Response(data={"ERROR" : serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
    
    
# @ /api/rooms/{roomId}/member/me : DELETE
# @ 탈퇴
class MemberByMeAPI(APIView):   
    # * DELETE /api/rooms/{roomId}/member/me
    # * 탈퇴
    @swagger_auto_schema(**rooms_id_member_me_delete)
    def delete(self, request, roomId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 내 정보 탐색
        try:
            room = Rooms.objects.get(id=roomId, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "해당 방이 존재하지 않습니다"}, 
                            status = status.HTTP_400_BAD_REQUEST)
            
        try:
            member = UsersRooms.objects.get(room_id=roomId, user_id=user.uid)
        except:
            return Response(data={"ERROR" : "잘못된 요청"}, 
                                status = status.HTTP_400_BAD_REQUEST)
        if member.deleted_at is not None:
            return Response(data={"ERROR" : "이미 탈퇴한 방입니다."}, 
                                status = status.HTTP_400_BAD_REQUEST)
            
        member.deleted_at = datetime.now()
        member.save()
        
        if not room.party_now:
            return Response(data={"ERROR" : "잘못된 정보"}, 
                                status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        room.party_now -= 1
        room.save()
        
        Notices.objects.create(
            user_id=room.user.uid, 
            message={
                "type" : "roomResign",
                "roomId" : room.pk,
                "message" : f"{member.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭을 탈퇴하였습니다."
            }
        )
        send_fcm_notification(
            user=room.user,
            title="카풀 멤버 탈퇴",
            body=f"{member.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭을 탈퇴하였습니다."
        )   
        
        roomChats = Chats.objects.filter(user=user)
        if roomChats.count() <= 0:
            return Response(data={"ERROR" : "채팅방이 존재하지 않음"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        myChat = None
        myDB = None
        cnt = None
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
                cnt = dict["chat_count"]
                myChat = roomChat
                myDB = db_ref
                break
        
        if myChat is None or myDB is None or cnt is None:
            return Response(data={"ERROR" : "채팅방이 존재하지 않음"}, 
                            status = status.HTTP_404_NOT_FOUND)   
        
        myChat.objects.update(load_until=cnt)
        myChat.save()
        
        myDB.update({
            "members": ArrayRemove([str(user.uid)])
        })
        
        return Response(status=status.HTTP_200_OK)

# @ /api/rooms/{roomId}/member/{memberId} : DELETE
# @ 강퇴
class MemberByIdAPI(APIView):
    # * DELETE /api/rooms/{roomId}/member/{memberId}
    # * 방 강퇴
    @swagger_auto_schema(**rooms_id_member_id_delete)
    def delete(self, request, roomId, memberId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 내 정보 탐색
        try:
            room = Rooms.objects.get(id=roomId, user_id=user.uid, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "해당 방에 대한 권한이 없습니다"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        try:
            member = UsersRooms.objects.get(room_id=roomId, user=memberId)
        except:
            return Response(data={"ERROR" : "잘못된 요청"}, 
                                status = status.HTTP_400_BAD_REQUEST)
        if member.deleted_at:
            return Response(data={"ERROR" : "방에 속하지 않은 멤버"}, 
                                status = status.HTTP_400_BAD_REQUEST)
            
        member.deleted_at = datetime.now()
        member.save()
        
        if not room.party_now:
            return Response(data={"ERROR" : "잘못된 정보"}, 
                                status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        room.party_now -= 1
        room.save()
        
        roomChats = Chats.objects.filter(user=member.user)
        if roomChats.count() <= 0:
            return Response(data={"ERROR" : "채팅방이 존재하지 않음"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        targetChat = None
        targetyDB = None
        cnt = None
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
                cnt = dict["chat_count"]
                targetChat = roomChat
                targetyDB = db_ref
                break
        
        if targetChat is None or targetyDB is None or cnt is None:
            return Response(data={"ERROR" : "채팅방이 존재하지 않음"}, 
                            status = status.HTTP_404_NOT_FOUND)   
        
        targetChat.objects.update(load_until=cnt)
        targetChat.save()
        
        targetyDB.update({
            "members": ArrayRemove([str(member.user.uid)])
        })
        
        return Response(status=status.HTTP_200_OK)