from django.contrib.auth import login
from rest_framework.response import Response            # DRF
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from firebase_admin import auth
from firebase.authentication import FirebaseAuthentication
from mota.models.users import Users
from mota.models.uid_dict import UidDict
from mota.serializers.users import *
from drf_yasg.utils import swagger_auto_schema
from swagger.views import login_get

from firebase_admin import messaging, firestore
import logging
db = firestore.client()

# @ /api/login : GET POST
# @ 로그인 정보를 확인하고, 없을경우 POST /api/login 수행
# * 참고 https://firebase.google.com/docs/auth/admin/manage-users?hl=ko

class LoginAPI(APIView):
    # permission_classes = [ IsAuthenticated ]
    # * Firebase Authentication 사용
    permission_classes = [ AllowAny ]
    firebase = FirebaseAuthentication()
    
    @swagger_auto_schema(**login_get)
    def get(self, request):
        # * 인증을 요청한 유저의 Firebase ID Token을 가진 유저 정보 생성 및 가져오기
        authUser = self.firebase.authenticate(request)
        if authUser is None:
            return Response(data={"ERROR" : "파이어베이스에서 토큰을 가져올 수 없음"},
                            status = status.HTTP_404_NOT_FOUND)

        isRegister = True
        
        uidDict, created = UidDict.objects.get_or_create(firebase=authUser[0])
        if created or uidDict.app is None:
            user = Users.objects.create()
            uidDict.app = user
            uidDict.save()
            with open("logs/account.log", "a", encoding="utf-8") as file:
                file.write(f"{authUser[0].username} {user.uid}\n")
            isRegister = False
        else:
            user = Users.objects.get(uid=uidDict.app.uid)
        
        if user.nickname is None:
            isRegister = False
        
        login(request, authUser[0])

        serializer = UsersGetSerializer(user)
        if not serializer:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # * Firebase auth 기반 JWT 토큰 생성
        additionalClaims = {
            'user': serializer.data,            # 유저 정보
            'isRegister': isRegister            # 가입 여부
        }
        JwtToken = auth.create_custom_token(authUser[0].username)
        res = [JwtToken, additionalClaims]
        
        return Response(data=res, 
                        status=status.HTTP_200_OK)