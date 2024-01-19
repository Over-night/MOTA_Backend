from rest_framework import serializers
from mota.models.terms import Terms

# @ 직렬 변환기 & 보기 추가 
# @ ModelSerializer는 중첩된 직렬 변환기에 대한 쓰기를 지원하지 않음 -> update() 및 create()를 재정의
# @ 사용자를 생성하기 위해 직접 API 요청을 사용하지 않음 -> update() 메서드만 덮어씀

# TODO : readonly 속성 설정하기 

# * Terms
class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Terms
        fields = '__all__'   

# # * RoomsPlan
# class RoomsPlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=RoomsPlan
#         fields = '__all__'   