from django.db import models
from mota.models.users import Users
from mota.models.rooms import Rooms

# @ users_reviews 테이블 : 리뷰 관리
class UsersReviews(models.Model):
    # * id              리뷰 식별 ID            INTEGER         PK, SERIAL
    # * userfrom        보내는 users 테이블     VARCHAR(255)    FK
    # * userto          받는 users 테이블       VARCHAR(255)    FK
    # * room            rooms 테이블            INTEGER         FK
    # * review          리뷰 세부 설정          VARCHAR(1000)   NN
    # * created_at      생성 일시               DATETIME        now()
    # * deleted_at      삭제 일시               DATETIME        DEF=null
    
    userfrom        = models.ForeignKey(Users,on_delete=models.CASCADE, related_name="userfrom")
    userto          = models.ForeignKey(Users,on_delete=models.CASCADE, related_name="userto")
    room            = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    review          = models.CharField(max_length=1000, null=False)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at      = models.DateTimeField(default=None, null=True, blank=True)
    
    class Meta:
        db_table = 'users_reviews'

# @ content
# * type : 리뷰의 종류
# *     "likes"     : 긍부정 여부
# *     "content"  : 글 작성
# * data : 리뷰의 내용
# *     likes : true-긍정/false-부정
# *     content : "내용"