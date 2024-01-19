from django.db import models
import uuid

# @ users 테이블 : 유저 정보 설정 
class Users(models.Model):
    # * uid             Firebase ID token의 UID     VARCHAR(255)    PK
    # * nickname        사용자 닉네임               VARCHAR(50)     BLK
    # * gender          사용자 성별                 VARCHAR(20)     BLK
    # * age             사용자 나이                 VARCHAR(20)     BLK
    # * picture         사진 링크                   TEXT            BLK
    # * blocked_until   차단 기간                   DATETIME        DEF=null        
    # * deleted_at      삭제 일시                   DATETIME        DEF=null
    
    # * django.contrib.auth.models User 
    # * id password last_login is_superuser username first_name last_name email is_staff is_active date_joined
    
    uid             = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    nickname        = models.CharField(max_length=50, blank=True)
    gender          = models.CharField(max_length=20, blank=True)
    age             = models.CharField(max_length=20, blank=True)
    picture         = models.TextField(blank=True)
    blocked_until   = models.DateTimeField(default=None, null=True, blank=True)
    deleted_at      = models.DateTimeField(default=None, null=True, blank=True)
    
    class Meta:
        db_table = 'users'
