from django.db import models
from mota.models.users import Users
from mota.models.rooms import Rooms

# @ users_approved 테이블 : 수락 여부   
class UsersFCM(models.Model):
    # ? Device 별 FCM 나중에 반영하기
    
    # * user            users 테이블            VARCHAR(255)    FK
    # * fcm_token       fcm 토큰                TEXT    
    # * updated_at      업데이트 일시           DATETIME
    
    user            = models.ForeignKey(Users,on_delete=models.CASCADE, primary_key=True)
    fcm_token       = models.TextField()
    updated_at      = models.DateTimeField(auto_now_add=True, auto_now=True)
    
    
    class Meta:
        db_table = 'users_fcm'