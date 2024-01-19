from rest_framework import serializers
from mota.models.users_approved import UsersApproved
from mota.models.users import Users


class ApproverSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(format='hex_verbose')
    
    class Meta:
        model=Users
        # fields = '__all__'
        fields=['uid', 'nickname', 'gender', 'age', 'picture']

# * UserApproved
class ApprovedSerializer(serializers.ModelSerializer):
    user = ApproverSerializer(many=False)
    class Meta:
        model=UsersApproved
        fields = '__all__'   