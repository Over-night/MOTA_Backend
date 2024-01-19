
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from mota.models.events_counter import EventsCounter

class ReviewsFromMeAPI(APIView):       
    # * POST /api/event
    # * 내가 작성한 리뷰 전부 조회 
    def post(self, request):
        if not "event_type" in request.data:
            return Response(data={"ERROR" : "잘못된 요청 전송됨"},
                                  status=status.HTTP_400_BAD_REQUEST)
        
        # 내가 작성했으면서, 삭제되지 않은 모든 글
        event, created = EventsCounter.objects.get_or_create(event_type=request.data["event_type"])
        if not created:
            event.event_count += 1
            event.save()
        
        return Response(status=status.HTTP_200_OK)