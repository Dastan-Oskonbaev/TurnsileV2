from rest_framework import viewsets
from .models import HistoryType, MembershipHistory
from .serializers import HistoryTypeSerializer, MembershipHistorySerializer


class HistoryTypeViewSet(viewsets.ModelViewSet):
    queryset = HistoryType.objects.all()
    serializer_class = HistoryTypeSerializer

# For future use
# class MembershipHistoryViewSet(viewsets.ModelViewSet):
#     queryset = MembershipHistory.objects.all()
#     serializer_class = MembershipHistorySerializer