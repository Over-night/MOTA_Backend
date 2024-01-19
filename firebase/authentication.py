import firebase_admin
from rest_framework.permissions import AllowAny
from firebase_admin import auth as firebase_auth, credentials
from rest_framework import authentication
from firebase import exceptions
from django.contrib.auth.models import User as AuthUser

# @ 환경변수
cred = credentials.Certificate("private/firebase.json")
default_app = firebase_admin.initialize_app(cred)

# @ FIREBASE AUTHENTICATION
class FirebaseAuthentication(authentication.BaseAuthentication):
    permission_classes = [ AllowAny ]
    
    def authenticate(self, request):
        # * 요청 헤더에서 ID 토큰을 가져옴
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise exceptions.NoAuthToken("인증 토큰이 주어지지 않음")
        
        # print('@@@@@@', request, auth_header)
        # * ID 토큰의 유효성 검사
        id_token = auth_header.split(" ").pop()
        print("@\n@\n", id_token, "\n@\n@")
        
        decoded_token = None
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.InvalidAuthToken("유효하지 않은 인증 토큰")

        if not id_token or not decoded_token:
            return None
        
        # * ID 토큰에서 uid를 가져옴 
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.FirebaseError()

        # * 임시 유저정보 생성 
        user, created = AuthUser.objects.get_or_create(username=uid)
        if created:
            user.email = decoded_token.get("email")
        # print(decoded_token.get("email"))
        return (user, None)
    
    def getUserFromToken(self, request):
        # * 요청 헤더에서 ID 토큰을 가져옴
        
        auth_header = request.headers.get('AUTHORIZATION', None)
        if not auth_header:
            raise exceptions.NoAuthToken("인증 토큰이 주어지지 않음")
    
        # * ID 토큰의 유효성 검사
        id_token = auth_header.split(" ").pop()
        
        decoded_token = None
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.InvalidAuthToken("유효하지 않은 인증 토큰")

        if not id_token or not decoded_token:
            return None
        
        # * ID 토큰에서 uid를 가져옴 
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.FirebaseError()

        # * 임시 유저정보 생성 
        user = AuthUser.objects.get(username=uid)
            
        return user