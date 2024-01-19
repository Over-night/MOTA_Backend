import imghdr, boto3
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mota.models.uid_dict import UidDict
from mota.models.users import Users
from mota.models.users_rooms import UsersRooms
from mota.models.rooms import Rooms
from mota.models.notices import Notices
from mota.models.users_approved import UsersApproved
from mota.serializers.users import *

from mota.utils import send_fcm_notification, load_user

from moyeobayo.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN

from swagger.views import users_me_get, users_me_put, users_me_delete, users_id_get

# @ /api/users/me : GET PUT DELETE
# @ 본인의 정보 확인

class UserMeAPI(APIView):
    img_format = [".jpg",".png",".jpeg",".JPG",".PNG","JPEG"]
    put_request = ["nickname", "gender", "age", "picture"]
    
    # * GET /api/users/me
    # * 내 정보 조회
    @swagger_auto_schema(**users_me_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 직렬화
        serializer = UsersGetSerializer(user)
        if not serializer:
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        # 반환
        return Response(serializer.data, 
                        status=status.HTTP_200_OK)
    
    # * PUT /api/users/me
    # * 내 정보 변경
    @swagger_auto_schema(**users_me_put)
    def put(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        if "nickname" in request.data: 
            if not isinstance(request.data["nickname"], str):
                return Response(data={"ERROR" : "nickname : 잘못된 자료형의 요청값"},
                                status=status.HTTP_400_BAD_REQUEST)
            user.nickname= request.data["nickname"].replace("\n", "")
        if "gender" in request.data:
            if not isinstance(request.data["gender"], str):
                return Response(data={"ERROR" : "gender : 잘못된 자료형의 요청값"},
                                status=status.HTTP_400_BAD_REQUEST)
            user.gender = request.data["gender"]
        if "age" in request.data:
            if not isinstance(request.data["age"], str):
                return Response(data={"ERROR" : "age : 잘못된 자료형의 요청값"},
                                status=status.HTTP_400_BAD_REQUEST)
            user.age = request.data["age"]
            
        if "picture" in request.FILES:
            image = request.FILES['picture']
            
            imageName = user.uid
            imagePath = f"media/profile-picture/{imageName}"
            
            s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            s3.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, imagePath, ExtraArgs={'ACL': 'public-read'})
        
            imageUrl = f"https://{AWS_S3_CUSTOM_DOMAIN}/{imagePath}"
            user.picture = imageUrl
            
        user.save()
        
        return Response(status=status.HTTP_200_OK)
    
    # 내 정보 삭제
    @swagger_auto_schema(**users_me_delete)
    def delete(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # * 방 삭제
        # ? 방 있는데 멋대로 탈퇴하면 안되지 않나
        roomsHost = Rooms.objects.filter(user_id=user.uid, 
                                     is_end=False, 
                                     deleted_at__isnull=True)
        for room in roomsHost:
            room.deleted_at = datetime.now()
            room.save()
        
            # 알림 전송 : 유저 
            # 알림 전송 
            members = UsersRooms.objects.filter(room_id=room.pk, deleted_at__isnull=True).values_list('user_id', flat=True)
            for member in members:
                Notices.objects.create(
                    user=member, 
                    message={
                        "type" : "roomCancel",
                        "roomId" : room.pk,
                        "message" : f"{room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀을 취소하였습니다."
                    }
                )
                send_fcm_notification(
                    user=member,
                    title="카풀 일정 취소",
                    body=f"{room.user.nickname} 님이 {room.plan_at.month}/{room.plan_at.day} {room.plan_at.hour}:{room.plan_at.minute}에 예정된 카풀을 취소하였습니다."
                )   
        
        # * 멤버 탈퇴
        roomsMember = UsersRooms.objects.filter(user_id=user.uid, deleted_at__isnull=True)
        for member in roomsMember:
            member.deleted_at = datetime.now()
            member.save()
        
            if not member.room.party_now:
                return Response(data={"ERROR" : "잘못된 정보"}, 
                                status = status.HTTP_500_INTERNAL_SERVER_ERROR)
            member.room.party_now -= 1
            member.room.save()
            
            Notices.objects.create(
                    user_id=member.user.uid, 
                    message={
                        "type" : "roomResign",
                        "roomId" : member.room.pk,
                        "message" : f"{user.nickname} 님이 {member.room.plan_at.month}/{member.room.plan_at.day} {member.room.plan_at.hour}:{member.room.plan_at.minute}에 예정된 카풀 매칭을 탈퇴하였습니다."
                    }
            )
            send_fcm_notification(
                user=member.user,
                title="카풀 멤버 탈퇴",
                body=f"{user.nickname} 님이 {member.room.plan_at.month}/{member.room.plan_at.day} {member.room.plan_at.hour}:{member.room.plan_at.minute}에 예정된 카풀 매칭을 탈퇴하였습니다."
            )   
            
        # * 가입 신청 취소
        approves = UsersApproved.objects.filter(user_id=user.uid)
        for approve in approves:
            approve.delete()
        
        # * 알림 삭제
        notices = Notices.objects.filter(user_id=user.uid)
        for notice in notices:
            notice.delete()
        
        user.deleted_at = datetime.now()
        user.save()
        dict = UidDict.objects.get(app=user)
        dict.app = None
        dict.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


# @ /api/users/{userId} : GET
# @ 특정 유저의 정보 확인
class UserOtherView(APIView):
    @swagger_auto_schema(**users_id_get)
    def get(self, request, userId):
        try:
            user = Users.objects.get(uid=userId)
        except:
            return Response(data={"ERROR" : "유저 정보가 없음"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsersGetSerializer(user)
        
        return Response(data=serializer.data, 
                        status=status.HTTP_200_OK)