from rest_framework import serializers
from mota.models.users_rooms import UsersRooms
from mota.models.users import Users

# * UserRooms
class MembersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=UsersRooms
        fields = '__all__'

# class MemberPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=UsersRooms
#         fields = ['room']