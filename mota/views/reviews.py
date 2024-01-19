from mota.serializers.reviews import *
from mota.models.users_reviews import UsersReviews
from mota.models.rooms import Rooms
from mota.models.users_rooms import UsersRooms
from mota.models.notices import Notices

from mota.utils import send_fcm_notification, load_user

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from swagger.views import reviews_post, reviews_id_get, reviews_id_put, reviews_id_delete, reviews_me_get


# @ /api/reviews : GET POST
# @ 내가 작성한 리뷰 - 전부 조회, 작성 
class ReviewsFromMeAPI(APIView):
    post_key = ["userto_id", "room_id", "review"]

    # * POST /api/reviews
    # * 리뷰 등록
    @swagger_auto_schema(**reviews_post)
    def post(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        if not all(key in request.data for key in self.post_key):
            return Response(data={"ERROR" : "잘못된 요청 전송됨"},
                                  status=status.HTTP_400_BAD_REQUEST)
        if user.uid == request.data["userto_id"]:
            return Response(data={"ERROR" : "리뷰를 작성할 대상이 자신임"},
                                  status=status.HTTP_400_BAD_REQUEST)
        
        # 현재 리뷰 작성 기준 : 카풀 일정을 넘겼을 경우
        try:
            room = Rooms.objects.get(id=request.data["room_id"], deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "유효하지 않은 요청"},
                                  status=status.HTTP_400_BAD_REQUEST)
        if not room.is_end:
            return Response(data={"ERROR" : "매칭이 종료되지 않았음"},
                                  status=status.HTTP_400_BAD_REQUEST)
            
        member = UsersRooms.objects.filter(room_id=request.data["room_id"], 
                                            user_id=user.uid,
                                            deleted_at__isnull=True)

        # 방장이 아니면서 멤버가 아닐 경우
        if room.user.uid != user.uid and not member:
            return Response(data={"ERROR" : "리뷰를 작성할 자격이 없음"},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        # 중복 작성 못하게  
        review, created = UsersReviews.objects.get_or_create(userfrom_id=user.uid, 
                                                             userto_id=request.data["userto_id"],
                                                             room_id=request.data["room_id"])
        if not created:
            if review.deleted_at is None:
                return Response(data={"ERROR" : "이미 리뷰가 작성됨"},
                                status=status.HTTP_400_BAD_REQUEST)
            review.deleted_at = None
        review.review = request.data["review"]
        review.save()
        
        Notices.objects.create(user_id=review.userto.uid, 
                                message={
                                    "type" : "reviewSend",
                                    "reviewId" : review.pk,
                                    "message" : f"새로운 리뷰가 작성되었습니다."
                                })
        send_fcm_notification(
            user=review.userto,
            title="리뷰 알림",
            body=f"새로운 리뷰가 작성되었습니다."
        )   
        
        return Response(status=status.HTTP_201_CREATED)


# @ /api/reviews/me : GET
# @ 내가 받은 리뷰 - 전부 조회
class ReviewsToMeAPI(APIView):  
    # * GET /api/reviews/me
    # * 내가 작성하거나 받은 리뷰 전부 조회 
    @swagger_auto_schema(**reviews_me_get)
    def get(self, request):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 내가 작성했거나 대상이면서, 삭제되지 않은 모든 글
        reviews = UsersReviews.objects.filter((Q(userfrom_id=user.uid) | Q(userto_id=user.uid)) &
                                              Q(deleted_at__isnull=True)
                                              ).order_by('-created_at')
        
        # 직렬화
        serializer = ReviewsSerializer(reviews, many=True)
        
        for data in serializer.data:
            data["isWriteByMe"] = True if data["userfrom"]["uid"] == str(user.uid) else False
        
        return Response(data = serializer.data,
                        status=status.HTTP_200_OK)
    
    
# @ /api/users/reviews/{id} : GET PUT DELETE
# @ 내가 작성한 특정 리뷰 조회,수정,삭제
class ReviewIdFromMeAPI(APIView): 
    # * GET /api/reviews/{reviewId}
    # * 내가 작성한 특정 리뷰 조회 
    @swagger_auto_schema(**reviews_id_get)
    def get(self, request, reviewId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        try:
            review = UsersReviews.objects.get(id=reviewId, userfrom_id=user.uid, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "리뷰 조회 실패"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        # 직렬화
        serializer = ReviewsSerializer(review)
        if not serializer:
            return Response(data={"ERROR" : serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
    
    # * PUT /api/reviews/{reviewId}
    # * 내가 작성한 특정 리뷰 수정 (3시간 이내)
    @swagger_auto_schema(**reviews_id_put)
    def put(self, request, reviewId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        # 내 리뷰가 아닐 경우 에러
        try:
            review = UsersReviews.objects.get(id=reviewId, userfrom_id=user.uid, deleted_at_isnull=True)
        except:
            return Response(data={"ERROR" : "리뷰에 대한 권한이 없음"},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not review.created_at:
            return Response(data={"ERROR" : "데이터에 이상이 있음"},
                            status=status.HTTP_400_BAD_REQUEST)
        if review.created_at + timedelta(hours=3) < datetime.now():
            return Response(data={"ERROR" : "수정할 수 있는 시간이 지남"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        review.review = request.data["review"]
        review.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    # * DELETE /api/reviews/{reviewId}
    # * 내가 작성한 특정 리뷰 삭제
    @swagger_auto_schema(**reviews_id_delete)
    def delete(self, request, reviewId):
        user = load_user(request)
        if user is None:
            return Response(data={"ERROR" : "파이어베이스 인증 및 유저 정보 조회 실패"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        
        try:
            review = UsersReviews.objects.get(id=reviewId, userfrom_id=user.uid)
        except:
            return Response(data={"ERROR" : "리뷰 조회 실패"}, 
                            status = status.HTTP_404_NOT_FOUND)
        
        # 리뷰가 이미 삭제되었을 경우
        if review.deleted_at:
            return Response(data={"ERROR" : "이미 삭제된 리뷰"},
                            status=status.HTTP_410_GONE)
        if not review.created_at:
            return Response(data={"ERROR" : "데이터에 이상이 있음"},
                            status=status.HTTP_400_BAD_REQUEST)
        if review.created_at + timedelta(hours=3) < datetime.now():
            return Response(data={"ERROR" : "삭제할 수 있는 시간이 지남"},
                            status=status.HTTP_400_BAD_REQUEST)
        review.deleted_at = datetime.now()
        review.save()
        
        return Response(status=status.HTTP_200_OK)