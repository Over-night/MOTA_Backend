from mota.serializer import TermsSerializer
from mota.models.terms import Terms
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

class TermsViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [ AllowAny ]
    
    queryset = Terms.objects.all()
    serializer_class = TermsSerializer

# Terms 목록 보여주기
terms_list = TermsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Terms detail 보여주기 + 수정 + 삭제
terms_detail = TermsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})