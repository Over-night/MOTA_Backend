from django.db import models
from django.contrib.auth.models import User as AuthUser
from mota.models.users import Users

class UidDict(models.Model):
    # * id              방 식별 ID              INTEGER         PK, SERIAL
    # * firebase        FB의 uid                VARCHAR(255)    FK
    # * app             app의 uid               JSONB           NN, BLK
    
    firebase        = models.ForeignKey(AuthUser,on_delete=models.CASCADE, null=False)
    app             = models.ForeignKey(Users,on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'uid_dict'

        