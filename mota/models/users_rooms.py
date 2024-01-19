from django.db import models
from mota.models.users import Users
from mota.models.rooms import Rooms

# @ users_room 테이블 : 방 정원 설정  
class UsersRooms(models.Model):
    # * id              일련번호                INTEGER         PK, SERIAL
    # * user            users 테이블            VARCHAR(255)    FK
    # * room            room의 id               INTEGER         FK       
    # * created_at      생성 일시               DATETIME        now()
    # * deleted_at      삭제 일시               DATETIME        DEF=null
    
    user            = models.ForeignKey(Users,on_delete=models.CASCADE)
    room            = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at      = models.DateTimeField(default=None, null=True, blank=True)
    
    class Meta:
        db_table = 'users_rooms'
        