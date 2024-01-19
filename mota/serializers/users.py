
from django.contrib.auth.models import User as AuthUser
from mota.models.users import Users
from rest_framework import serializers

# @ 직렬 변환기 & 보기 추가 

# @ GET
class UsersGetSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(format='hex_verbose')
    class Meta:
        model=Users
        # fields = '__all__'
        fields=['uid', 'nickname', 'gender', 'age', 'picture', 'blocked_until', 'deleted_at']

# * django.contrib.auth.models User
# class AuthUserGetSerializer(serializers.ModelSerializer):
#     users = UsersGetSerializer(many=False)
#     class Meta:
#         model=AuthUser
#         # fields = '__all__'
#         fields=['id', 'email', 'date_joined', 'last_login']
        

# @ PUT
class UsersPutSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        # fields = '__all__'
        fields=['nickname', 'gender', 'age', 'picture']
        