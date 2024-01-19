from django.db import models

# @ terms 테이블 : 약관 정보 설정 
class Terms(models.Model):
    # * name            약관 이름           VARCHAR(50)
    # * isEssential     필수 동의 여부      boolean
    # * content         약관 내용           TEXT              
    # * created_at      생성 일시           DATETIME        now()
    # * updated_at      수정 일시           DATETIME        now()
    # * deleted_at      삭제 일시           DATETIME        null
    
    
    name            = models.CharField()
    isEssential     = models.BooleanField()
    content         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    updated_at      = models.DateTimeField(auto_now=True)
    deleted_at      = models.DateTimeField(null=True, default=None, blank=True)
    
    class Meta:
        db_table = 'terms'