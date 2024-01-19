from rest_framework import serializers
from mota.models.users_driver import UsersDriver

# * UserDriver
class DriverGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=UsersDriver
        fields = '__all__'   
        
class DriverPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=UsersDriver
        fields = '__all__'