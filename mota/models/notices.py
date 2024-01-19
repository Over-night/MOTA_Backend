from django.db import models
from mota.models.users import Users

# @ notices 테이블 : 알림 설정 
class Notices(models.Model):
    # * id              방 식별 ID              INTEGER         PK, SERIAL
    # * user            users 테이블            VARCHAR(255)    FK
    # * message         알림 내용               JSONB           NN, BLK
    # * created_at      생성 일시               DATETIME
    # * read_at         열람 일시               DATETIME        DEF=null
    
    user            = models.ForeignKey(Users,on_delete=models.CASCADE, null=False)
    message         = models.JSONField('json', default=dict, null=False, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    read_at         = models.DateTimeField(default=None, null=True)
    
    class Meta:
        db_table = 'notices'


'''
공식 json
{
   "to": "FCM_TOKEN",
   "notification": {
      "title": "Sample Title",
      "body": "Sample body text"
   },
   "data": {
      "key1": "value1",
      "key2": "value2"
   }
}
'''