from django.db import models
from mota.models.users import Users 
import uuid

# @ chat 테이블 : 채팅 설정
class Chats(models.Model):
    # * id                                              SERIAL          PK
    # * chat_uuid       채팅 식별 ID                    UUID            
    # * chat_name       채팅방명                        VARCHAR(100)        
    # * user            해당 유저                       UUID            FK
    # * read_until      읽은 메시지 범위                INTEGER         DEF=0
    # * load_since      열람 가능한 메시지 시작 범위    INTEGER         DEF=0
    # * load_until      열람 가능한 메시지 끝 범위      INTEGER         DEF=None
    # * will_notify     알림 여부                       BOOLEAN         DEF=T
    
    chat_uuid       = models.UUIDField(default=uuid.uuid4, editable=False)
    chat_name       = models.CharField(max_length=100, blank=True)
    user            = models.ForeignKey(Users,on_delete=models.CASCADE, null=False)
    read_until      = models.IntegerField(default=0, blank=True)
    load_since      = models.IntegerField(default=0, blank=True)
    load_until      = models.IntegerField(default=None, null=True, blank=True)
    will_notify     = models.BooleanField(default=True, blank=True)
    
    class Meta:
        db_table = 'chats'
        
'''
{
    "room_id": ll,
    "members" : [1, 2, 3, 4]
    "chat_count": n,
    "last_chat": "~~~"
    "is_end": T/F,
    "created_at": 시간,
    "updated_at": 시간,
}
{
    "messages": [
        {
            "id": serial
            "timestamp": 시간,
            "sender": 사용자 UUID,
            "text": 메시지,
            "file": url
        },
    ]
}
'''
