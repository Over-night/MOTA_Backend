from django.db import models
from django.contrib.postgres.fields import ArrayField
from mota.models.users import Users

# @ users_driver 테이블 : 유저 운전자 정보 관리
class UsersDriver(models.Model):
    # * user          유저 uid              VARCHAR(255)    PK
    # * car_no        차량 번호             VARCHAR(20)     NN, BLK
    # * car_type      차량 종류             VARCHAR(20)     NN, BLK
    # * car_limit     최대 탑승가능인원     INTEGER         DEF=3, BLK
    # * car_pictures  사진 링크             ARRAY(TEXT)     BLK
    # * license_path  면허증 경로           TEXT            NN        
    # * license_at    등록 일시             DATETIME        now()
    
    # * django.contrib.auth.models User 
    # * id password last_login is_superuser username first_name last_name email is_staff is_active date_joined
    
    user            = models.OneToOneField(Users,on_delete=models.CASCADE, primary_key=True)
    car_no          = models.CharField(max_length=20, null=False, blank=True)
    car_type        = models.CharField(max_length=20, null=False, blank=True)
    car_limit       = models.IntegerField(default=3, blank=True)
    car_pictures    = ArrayField(models.TextField(), blank=True)
    license_path    = models.TextField(null=False)
    license_at      = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        db_table = 'users_driver'
        