from mota.models.notices import Notices
from rest_framework import serializers

class NoticeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notices
        fields = '__all__'
        