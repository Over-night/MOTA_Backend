from mota.models.rooms import Rooms
from mota.models.users import Users
from rest_framework import serializers

# * Rooms
class RoomsHostSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(format='hex_verbose')
    class Meta:
        model=Users
        # fields = '__all__'
        fields=['uid', 'nickname', 'gender', 'age', 'picture']
        
class RoomsGetSerializer(serializers.ModelSerializer):
    user = RoomsHostSerializer(many=False)
    class Meta:
        model=Rooms
        fields = ['id', 'user', 'price', 'party_limit', 'party_now', 'locate_start', 'locate_end', 'plan_at', 'content', 'option', 'is_end', 'created_at', 'deleted_at']
       
# class RoomPlanSerializer(serializers.ModelSerializer):
#     room = RoomsGetSerializer(many=True)
#     class Meta:
#         model=RoomsPlan
#         fields=['room', 'plan_at']       
        
class RoomsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rooms
        # fields = '__all__'
        fields=['price', 'party_limit', 'locate_start', 'locate_end', 'content', 'option']
        
class RoomsPutSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rooms
        # fields = '__all__'
        fields=['price', 'content', 'age', 'picture']