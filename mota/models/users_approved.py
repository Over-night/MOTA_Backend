from django.db import models
from mota.models.users import Users
from mota.models.rooms import Rooms

# @ users_approved 테이블 : 수락 여부   
class UsersApproved(models.Model):
    # * id              일련번호                INTEGER         PK, SERIAL
    # * user            users 테이블            VARCHAR(255)    FK
    # * room            room의 id               INTEGER         FK
    # * prove           수락 여부               VARCHAR(20)     DEF="wait"
    # * update_at       업데이트 시간           DATETIME        auto_now
    
    user            = models.ForeignKey(Users,on_delete=models.CASCADE)
    room            = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    prove           = models.CharField(max_length=20, default="wait")
    updated_at      = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_approved'

# * prove
#       "wait"      : 대기
#       "proved"    : 승인
#       "disproved" : 거절