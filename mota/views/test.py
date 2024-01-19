# from django.test import TestCase, RequestFactory
from mota.models.rooms import Rooms
from mota.models.users_rooms import UsersRooms
from mota.models.notices import Notices
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from swagger.views import test_carpool_terminate
from rest_framework import status


# @ /api/test/room-terminate/id : PUT
# @ # 방 전체 조회 및 생성
class TestRoomsTerminateAPI(APIView):
    
    # * PUT /api/test/room-terminate/{termId}
    # * 방 강제 종료 진행 
    @swagger_auto_schema(**test_carpool_terminate)
    def put(self, request, termId):
        try:
            room = Rooms.objects.get(id=termId, is_end=False, deleted_at__isnull=True)
        except:
            return Response(data={"ERROR" : "방 없음"}, 
                            status = status.HTTP_401_UNAUTHORIZED)
        room.is_end = True
        room.save()
        
        # 알림 전송 : 방장
        Notices.objects.create(user_id=room.user.uid, 
                               message={
                                    "type" : "myRoomEnd",
                                    "roomId" : room.pk,
                                    "message" : f"카풀 {room.pk}이 종료되었습니다.",
                                    "url" : "https://docs.google.com/forms/d/e/1FAIpQLScTwqda5ffvsimCm8DpxLNRZL-ipBwgn1aTrtHSVCXL3l6zwg/viewform?usp=sf_link"}
                               )
        
        # 알림 전송 : 유저 
        users = UsersRooms.objects.filter(room_id=room.pk, deleted_at__isnull=True)
        for user in users:
            Notices.objects.create(user_id=user.user.uid,
                               message={
                                    "type" : "roomEnd",
                                    "roomId" : room.pk,
                                    "message" : f"카풀 {room.pk}이 종료되었습니다.",
                                    "url" : "https://docs.google.com/forms/d/e/1FAIpQLScTwqda5ffvsimCm8DpxLNRZL-ipBwgn1aTrtHSVCXL3l6zwg/viewform?usp=sf_link"}
                               )

        return Response(status=status.HTTP_200_OK)


# import random, string

# from mota.models.users import Users
# from django.contrib.auth.models import User as AuthUser

# # * 랜덤 문자열 생성
# def generator_randomString(n):
#     stringPool = string.ascii_letters + string.digits
#     return ''.join(random.choice(stringPool) for _ in range(n))
        
# class Test_Login(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.userAuth = AuthUser.objects.create(namusernamee=generator_randomString(28))
#         self.user = Users.objects.create(uid=self.userAuth.username, user_id=self.userAuth)


#     def test_name_label(self):
#         requset = self.factory


#     def test_age_bigger_19(self):

#         age = Member.objects.get(name='byeonguk').age

#         check_age = age > 19

#         self.assertTrue(check_age)