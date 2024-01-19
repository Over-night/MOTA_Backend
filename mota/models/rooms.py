from django.db import models
from mota.models.users import Users

# TODO : user 이름 변경 
# @ rooms 테이블 : 매칭방 정보 설정 
class Rooms(models.Model):
    # * id              방 식별 ID              INTEGER         PK, SERIAL
    # * user            users 테이블            VARCHAR(255)    FK
    # * price           인원 당 가격            INTEGER         DEF=0, BLK
    # * party_limit     탑승 가능 인원 제한     INTEGER         DEF=3, BLK
    # * party_now       남은 탑승 가능 인원     INTEGER         BLK
    # * locate_start    출발지                  VARCHAR(100)    NN, BLK
    # * locate_end      도착지                  VARCHAR(100)    NN, BLK
    # * plan_at         일정                    DATETIME        NN
    # * content         상세 내용               TEXT            BLK
    # * option          세부 설정               JSONB           NN, BLK
    # * is_end          종료 여부               BOOLEAN         DEF=false     
    # * created_at      생성 일시               DATETIME        now()
    # * deleted_at      삭제 일시               DATETIME        DEF=null
    
    user            = models.ForeignKey(Users,on_delete=models.CASCADE)
    price           = models.IntegerField(default=0, blank=True)
    party_limit     = models.IntegerField(default=3, blank=True)
    party_now       = models.IntegerField(default=0, blank=True, null=True)
    locate_start    = models.CharField(max_length=100, null=False, blank=True)
    locate_end      = models.CharField(max_length=100, null=False, blank=True)
    plan_at         = models.DateTimeField(null=False, blank=True)
    content         = models.TextField(blank=True)
    option          = models.JSONField('json', default=dict, null=False, blank=True)
    is_end          = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at      = models.DateTimeField(default=None, null=True, blank=True)
    
    class Meta:
        db_table = 'rooms'
        
# @ option
# * gender : 성별 관련
#       "male"      : 남성만
#       "female"    : 여성만
#       "anybody"   : 상관없음
# * age    : 나이 관련
#       "xtoy"      : x살대부터 y살대까지
#       "anybody"   : 상관없음


# ! For MVP, This structure will not used
# from django.db import models
# from mota.models.users import Users

# # @ rooms 테이블 : 매칭방 정보 설정 
# class Rooms(models.Model):
#     # * id              방 식별 ID              INTEGER         PK, SERIAL
#     # * user            users 테이블            VARCHAR(255)    FK
#     # * price           인원 당 가격            INTEGER         DEF=0, BLK
#     # * party_limit     탑승 가능 인원 제한     INTEGER         DEF=3, BLK
#     # * party_now       남은 탑승 가능 인원     INTEGER         BLK
#     # * locate_start    출발지                  VARCHAR(100)    NN, BLK
#     # * locate_end      도착지                  VARCHAR(100)    NN, BLK
#     # * content         상세 내영               TEXT            BLK
#     # * option          세부 설정               JSONB           NN, BLK     
#     # * created_at      생성 일시               DATETIME        now()
#     # * deleted_at      삭제 일시               DATETIME        DEF=null
    
#     user            = models.ForeignKey(Users,on_delete=models.CASCADE)
#     price           = models.IntegerField(default=0, blank=True)
#     party_limit     = models.IntegerField(default=3, blank=True)
#     party_now       = models.IntegerField(default=0, blank=True, null=True)
#     locate_start    = models.CharField(max_length=100, null=False, blank=True)
#     locate_end      = models.CharField(max_length=100, null=False, blank=True)
#     content         = models.TextField(blank=True)
#     option          = models.JSONField('json', default=dict, null=False, blank=True)
#     created_at      = models.DateTimeField(auto_now_add=True, null=True)
#     deleted_at      = models.DateTimeField(default=None, null=True)
    
#     class Meta:
#         db_table = 'rooms'
        
# # @ option
# # * gender : 성별 관련
# #       "male"      : 남성만
# #       "female"    : 여성만
# #       "anybody"   : 상관없음
# # * age    : 나이 관련
# #       "xtoy"      : x살대부터 y살대까지
# #       "anybody"   : 상관없음