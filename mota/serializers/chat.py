from mota.models.chats import Chats
from rest_framework import serializers

class ChatsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Chats
        fields = '__all__'