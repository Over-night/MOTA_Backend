from mota.serializers.approved import *
from mota.models.users import Users
from mota.models.users_approved import UsersApproved
from mota.models.users_rooms import UsersRooms
from mota.models.rooms import Rooms
from mota.models.notices import Notices
from mota.models.chats import Chats

from mota.utils import send_fcm_notification, load_user


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from firebase_admin import firestore
from google.cloud.firestore import ArrayUnion

from drf_yasg.utils import swagger_auto_schema
from swagger.views import rooms_id_approval_get, rooms_id_approval_post, rooms_id_approval_id_get, rooms_id_approval_id_put, rooms_id_approval_id_delete, rooms_me_approval_get, rooms_me_approval_id_delete

db = firestore.client()

# @ /api/rooms/{roomId}/approval : GET POST
# @ 승인 조회 / 등록
class ApproveAPI(APIView):
    # * GET /api/rooms/{roomId}/approval
    # * 현재 방의 신청 정보 전부 조회
    @swagger_auto_schema(**rooms_id_approval_get)
    def get(self, request, roomId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 방이 유효한지, 방장인지
        try:
            room = Rooms.objects.get(id=roomId, user_id=user.uid, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "방 정보를 찾을 수 없음"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        # 신청이 있는지
        approves = UsersApproved.objects.filter(room_id=room.pk, prove="wait")
        if not approves:
            return Response(data={"ERROR" : "신청 정보 없음"},
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = ApprovedSerializer(approves, many=True)
        if not serializer:
            return Response(data={"ERROR" : serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
    
    # * POST /api/rooms/{roomId}/approval
    # * 승인 신청
    @swagger_auto_schema(**rooms_id_approval_post)
    def post(self, request, roomId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
         
        # 방이 유효한지
        try:
            room = Rooms.objects.get(id=roomId, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "방 정보를 찾을 수 없음"}, 
                            status=status.HTTP_404_NOT_FOUND)
        # 방장이 아닌지
        if room.user.uid == user.uid:
            return Response(data={"ERROR" : "해당 방의 방장임"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        # 멤버가 아닌지
        member = UsersRooms.objects.filter(room_id=roomId, user_id=user.uid, deleted_at__isnull=True)
        if member.count() > 0:
            return Response(data={"ERROR" : "이미 가입된 상태"}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        # 이미 신청했는지, 모두 아닐 경우 생성
        approves, created = UsersApproved.objects.get_or_create(room_id=room.pk, user_id=user.uid)
        if not created:
            # 신청중일 경우
            if approves.prove=="wait":
                return Response(data={"ERROR" : "이미 신청했거나 거절된지 얼마 안되었음"},
                                status=status.HTTP_400_BAD_REQUEST)
            # 신청중이 아닐 경우 
            approves.prove="wait"
            approves.save()
        
        # 알림 전송 : room 참여 이벤트 발생 시 운전자에게 알림 전송
        Notices.objects.create(user_id=room.user.uid, 
                                message={
                                    "type" : "joinRequest",
                                    "userId" : str(room.user.uid),
                                    "roomId" : roomId,
                                    "approveId": approves.pk,
                                    "message" : f"{user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭에 가입을 요청하였습니다."
                                })
        send_fcm_notification(
            user=room.user,
            title="매칭 가입 요청",
            body=f"{user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭에 가입을 요청하였습니다."
        )   
        
        return Response(status=status.HTTP_201_CREATED)
    
# @ /api/rooms/{roomId}/approval/{approvalId} : GET PUT DELETE
# @ 특정 가입 요청 정보 조회 
class ApproveByIdAPI(APIView):    
    # * GET /api/rooms/{roomId}/approval/{approvalId}
    # * 특정 방의 특정 신청 요청 조회
    @swagger_auto_schema(**rooms_id_approval_id_get)
    def get(self, request, roomId, approvalId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 요청 정보 취득
        try:
            approve = UsersApproved.objects.get(id=approvalId, room_id=roomId, prove="wait")
        except:
            return Response(data={"ERROR" : "가입 요청 정보를 찾을 수 없음"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        # 유효성 및 권한 확인
        if approve.room.user.uid != user.uid:
            return Response(data={"ERROR" : "가입 요청 정보를 조회할 권한 없음"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
            
        serializer = ApprovedSerializer(approve)
        if not serializer:
            return Response(data={"ERROR" : serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=serializer.data, 
                        status=status.HTTP_200_OK)
    
    # * PUT /api/rooms/{roomId}/approval/{approvalId}
    # * 특정 방의 특정 신청 상태 업데이트
    @swagger_auto_schema(**rooms_id_approval_id_put)
    def put(self, request, roomId, approvalId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 요청 확인
        if not "prove" in request.data:
            return Response(data={"ERROR" : "잘못된 요청"}, 
                            status = status.HTTP_400_BAD_REQUEST)
        
        # 요청 정보 취득
        try:
            approve = UsersApproved.objects.get(id=approvalId, room_id=roomId, prove="wait")
        except:
            return Response(data={"ERROR" : "가입 요청 정보를 찾을 수 없음"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        # 유효성 및 권한 확인
        if approve.room.user.uid != user.uid:
            return Response(data={"ERROR" : "가입 요청 정보를 조회할 권한 없음"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            room = Rooms.objects.get(id=roomId, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "해당 방이 존재하지 않습니다"}, 
                            status = status.HTTP_404_NOT_FOUND)
        if room.party_now is None or room.party_limit is None:
            return Response(data={"ERROR" : "방 데이터에 오류 발생"}, 
                            status = status.HTTP_400_BAD_REQUEST)
            
        
        # 가입 승인이 거절될 경우 
        if request.data["prove"] != 'proved':
            approve.prove = request.data["prove"]
            approve.save()
            # 알림 생성
            
            Notices.objects.create(user_id=approve.user.uid, 
                                message={
                                    "type" : "joinDisapproved",
                                    "roomId" : roomId,
                                    "message" : f"{approve.room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭의 가입요청에 거절하였습니다."
                                })
            send_fcm_notification(
                user=approve.user,
                title="가입 요청 거절",
                body=f"{approve.room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭의 가입요청에 거절하였습니다."
            )   
        
            return Response(status=status.HTTP_204_NO_CONTENT)

        if room.party_now >= room.party_limit:
            return Response(data={"ERROR" : "방의 정원이 만원입니다."}, 
                            status = status.HTTP_400_BAD_REQUEST)
        
        # 내 정보 탐색
        meInMenber, created = UsersRooms.objects.get_or_create(room_id=roomId, user_id=approve.user.uid)
        # 재가입일 경우 deleted_at = null
        if not created:
            if meInMenber.deleted_at is None:
                return Response(data={"ERROR" : "이미 가입된 상태"}, 
                                status = status.HTTP_400_BAD_REQUEST)
            else:
                meInMenber.deleted_at = None
                meInMenber.save()
        
        # 인원 추가 절차 진행
        room.party_now += 1
        room.save()
        
        # 알림 생성
        Notices.objects.create(user_id=approve.user.uid, 
                               message={
                                    "type" : "joinApproved",
                                    "roomId" : roomId,
                                    "message" : f"{approve.room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭의 가입요청을 수락하였습니다."}
                               )
        send_fcm_notification(
            user=approve.user,
            title="가입 요청 수락",
            body=f"{approve.room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭의 가입요청을 수락하였습니다."
        )   
        
        # 상태 반영 
        approve.prove = request.data["prove"]
        approve.save()
        
        roomChats = Chats.objects.filter(user=room.user)
        if roomChats.count() <= 0:
            return Response(data={"ERROR" : "채팅방이 존재하지 않음"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        myChat = None
        myDB = None
        cnt = None
        for roomChat in roomChats:
            dbInfo_ref = db.collection('chat_info').document(str(roomChat.chat_uuid))
            try:
                dbInfo_data = dbInfo_ref.get()
            except:
                continue
            if not dbInfo_data.exists:
                continue
            
            dbInfo_dict = dbInfo_data.to_dict()
            if dbInfo_dict["room_id"] == room.pk:
                cnt = dbInfo_dict["chat_count"]
                myChat = roomChat
                myDB = dbInfo_ref
                break
        
        if myChat is None or myDB is None or cnt is None:
            return Response(data={"ERROR" : "채팅방이 존재하지 않음"}, 
                            status = status.HTTP_404_NOT_FOUND)   
        
        try:
            getMyRoom = Chats.objects.get(chat_uuid=myChat.chat_uuid, user=approve.user)
            getMyRoom.objects.update(load_since=cnt-1 if cnt > 0 else 0, load_until=None)
            getMyRoom.save()
        except:
            myRoom = Chats.objects.create(chat_uuid=myChat.chat_uuid, 
                                          chat_name=myChat.chat_name, 
                                          user=approve.user, 
                                          load_since=cnt-1 if cnt > 0 else 0)
        
        myDB.update({
            "members": ArrayUnion([str(approve.user.uid)])
        })
        
        # * 수락 정보 제거
        willRejects = UsersApproved.objects.filter(room_id=roomId, prove="wait")
        for approve in willRejects:
            approve.prove = "disproved"
            approve.save()
            
            # 알림 생성
            Notices.objects.create(user_id=approve.user.uid, 
                                message={
                                    "type" : "joinDisapproved",
                                    "roomId" : roomId,
                                    "message" : f"{approve.room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭의 가입요청에 거절하였습니다."
                                })
            send_fcm_notification(
                user=approve.user,
                title="가입 요청 거절",
                body=f"{approve.room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀 매칭의 가입요청에 거절하였습니다."
            )   
        
        return Response(status=status.HTTP_200_OK)
    
    # * DELETE /api/rooms/{roomId}/approval/{approvalId}
    # * 특정 방의 신청 요청 삭제
    @swagger_auto_schema(**rooms_id_approval_id_delete)
    def delete(self, request, roomId, approvalId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
            
        # 요청 정보 취득
        try:
            approve = UsersApproved.objects.get(id=approvalId, room_id=roomId, prove="wait")
        except:
            return Response(data={"ERROR" : "가입 요청 정보를 찾을 수 없음"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        # 유효성 및 권한 확인
        if approve.user.uid != user.uid:
            return Response(data={"ERROR" : "가입 요청 정보를 삭제할 권한 없음"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        
        approve.delete()
        
        return Response(status=status.HTTP_200_OK)
    
# @ /api/rooms/me/approval : GET
# @ 나의 가입 요청들 조회 
class ApprovesByMeAPI(APIView):   
    # * GET /api/rooms/me/approval
    # * 내 신청 목록 조회
    @swagger_auto_schema(**rooms_me_approval_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 요청 정보 취득 (모든)
        myApproves = UsersApproved.objects.filter(user_id=user.uid)
        myRooms = Rooms.objects.filter(user_id=user.uid, is_end=False).values_list('id', flat=True)
        roomApproves = UsersApproved.objects.filter(room_id__in=myRooms, prove="wait")
        
        meSerializer = ApprovedSerializer(myApproves, many=True)
        if not meSerializer:
            return Response(data={"ERROR" : meSerializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        roomSerializer = ApprovedSerializer(roomApproves, many=True)
        if not meSerializer:
            return Response(data={"ERROR" : roomSerializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        result = []
        for data in meSerializer.data:
            data["type"]="ApplyByMe"
            result.append(data)
        for data in roomSerializer.data:
            data["type"]="ApplyByElse"
            result.append(data)
        
        return Response(data=result,
                        status=status.HTTP_200_OK)
        
# @ /api/rooms/me/approval/{approvalId} : delete
# @ 나의 특정 가입 요청 정보 조회 
class ApproveByMeAPI(APIView):
    # * GET /api/rooms/me/approval/{approvalId}
    # * 특정 가입 요청에 대해 취소 절차 진행
    @swagger_auto_schema(**rooms_me_approval_id_delete)
    def delete(self, request, approvalId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 요청 정보 취득
        try:
            myApprove = UsersApproved.objects.get(id=approvalId, user_id=user.uid, prove='wait')
        except:
            return Response(data={"ERROR" : "요청 정보 조회 실패"}, 
                            status = status.HTTP_404_NOT_FOUND)
       
        myApprove.delete()
        
        return Response(status=status.HTTP_200_OK)