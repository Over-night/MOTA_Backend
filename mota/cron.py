from django.db.models import Q
from mota.models.rooms import Rooms
from mota.models.users_rooms import UsersRooms
from mota.models.notices import Notices
from mota.models.users_approved import UsersApproved
from django.utils.timezone import now
from datetime import timedelta


def carpool_end():
    # 운행 예정 시각보다 하루 후인 모든 카풀 종료
    one_days_after = now() - timedelta(days=1)
    roomsBeEnd = Rooms.objects.filter(is_end=False, deleted_at__isnull=True, plan_at__lte=one_days_after)
    
    for room in roomsBeEnd:
        # 방 종료
        room.is_end = True
        room.save()
        
        # 알림 전송 : 방장
        Notices.objects.create(user_id=room.user.uid, 
                               message={
                                    "type" : "myRoomEnd",
                                    "roomId" : room.pk,
                                    "message" : f"카풀 {room.pk}이 종료되었습니다."}
                               )
        
        # 알림 전송 : 유저 
        users = UsersRooms.objects.filter(room_id=room.pk, deleted_at__isnull=True)
        for user in users:
            Notices.objects.create(user_id=user.user.uid,
                               message={
                                    "type" : "roomEnd",
                                    "roomId" : room.pk,
                                    "message" : f"카풀 {room.pk}이 종료되었습니다."}
                               )
        
        print(f"{room.pk} {now()}")
    
    
# ? : 알림 기록을 저장할까    
def notices_delete():
    # 알림이 전송된지 7일이 지났거나 읽은지 1일이 지난 모든 알림 삭제
    one_day_ago = now() - timedelta(days=1)
    seven_days_ago = now() - timedelta(days=7)
    
    noticesBeDeleted = Notices.objects.filter(
        Q(read_at__lte=one_day_ago) | Q(created_at__lte=seven_days_ago)
    )
    
    noticesBeDeleted.delete()

def approved_delete():
    # 요청이 반영된지 3일이 지난 모든 카풀 삭제
    three_days_ago = now() - timedelta(days=3)
    half_years_ago = now() - timedelta(days=180)
    
    noticesBeDeleted = UsersApproved.objects.filter(
        (Q(prove__exact="wait") & Q(updated_at__lte=three_days_ago)) |
        Q(updated_at__lte=half_years_ago)
    )
    
    noticesBeDeleted.delete()