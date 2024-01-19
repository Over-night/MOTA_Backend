from rest_framework import status
from rest_framework.exceptions import APIException


class NoAuthToken(APIException):
        status_code = status.HTTP_401_UNAUTHORIZED
        default_detail = "인증 토큰이 주어지지 않음"
        default_code = "no_auth_token"
class InvalidAuthToken(APIException):
        status_code = status.HTTP_401_UNAUTHORIZED
        default_detail = "유효하지 않은 인증 토큰"
        default_code = "invalid_token"
class FirebaseError(APIException):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        default_detail = "인증토큰이 파이어베이스의 UID 정보를 가지고 있지 않음"
        default_code = "no_firebase_uid"