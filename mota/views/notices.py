from mota.serializers.notices import *
from mota.models.notices import Notices
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from mota.utils import load_user

from drf_yasg.utils import swagger_auto_schema
from swagger.views import notice_get, notice_put, notice_id_put
from django.utils import timezone

# @ /api/users/me/notice : GET
# @ 알림 정보
class NoticeAPI(APIView):
    # * GET /api/notices
    # * 알림 정보 전체 조회
    @swagger_auto_schema(**notice_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        
        notices = Notices.objects.filter(user_id=user.uid).order_by('-created_at')
        
        serializer = NoticeGetSerializer(notices, many=True)
        
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
        
    # * PUT /api/notices
    # * 알림 정보 전체 읽음 처리
    @swagger_auto_schema(**notice_put)
    def put(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        notices = Notices.objects.filter(user_id=user.uid, read_at__isnull=True)
        notices.update(read_at=timezone.now())
        
        return Response(status=status.HTTP_200_OK)
        
        
# @ /api/users/me/notice/{id} : GET
# @ 특정 알림 정보
class NoticeByIdAPI(APIView):
    # * PUT /api/notices/{noticeId}
    # * 알림 읽음 처리
    @swagger_auto_schema(**notice_id_put)
    def put(self, request, noticeId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
            
        # 알림을 읽었는지 
        try:
            notice = Notices.objects.get(id=noticeId, user_id=user.uid)
        except:
            return Response(data={"ERROR" : "정보를 찾을 수 없음"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        notice.read_at = timezone.now()
        notice.save()
        
        return Response(status=status.HTTP_200_OK)