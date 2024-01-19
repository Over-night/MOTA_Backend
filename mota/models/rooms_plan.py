
# ! For MVP, This structure will not used
# from django.db import models
# from mota.models.rooms import Rooms

# # @ rooms_plan 테이블 : 방 계획 설정

# class RoomsPlan(models.Model):
#     # * id              일련번호                INTEGER         PK, SERIAL
#     # * room            users 테이블            INTEGER         FK
#     # * plan_at         일정                    DATETIME        NN, BLK
#     # * is_reverse      출-도착지 반전 여부     BOOLEAN         DEF=False, BLK
#     # * deleted_at      삭제 일시               DATETIME        DEF=null
    
#     room            = models.ForeignKey(Rooms,on_delete=models.CASCADE)
#     plan_at         = models.DateTimeField(null=False, blank=True)
#     is_reverse      = models.BooleanField(default=False, blank=True)
#     deleted_at      = models.DateTimeField(default=None, null=True)
    
#     class Meta:
#         db_table = 'rooms_plan'
        