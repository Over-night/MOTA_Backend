from django.db import models

# @ users_driver 테이블 : 유저 운전자 정보 관리
class EventsCounter(models.Model):    
    # * id                  일련번호                INTEGER         PK, SERIAL
    # * event_type          이벤트 타입             VARCHAR(255)        
    # * event_count         이벤트 발생횟수         BIGINT          DEF=0

    event_type           = models.CharField(max_length=100, null=False)
    event_count          = models.BigIntegerField(default=0, blank=True)
    
    class Meta:
        db_table = 'events_counter'