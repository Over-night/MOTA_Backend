from rest_framework import serializers
from mota.models.users_reviews import UsersReviews
from mota.serializers.users import *

             
class ReviewsSerializer(serializers.ModelSerializer):
    userfrom = UsersGetSerializer(many=False)
    userto = UsersGetSerializer(many=False)
    class Meta:
        model=UsersReviews
        fields = ['id', 'userfrom', 'userto', 'room', 'review', 'created_at', 'deleted_at']