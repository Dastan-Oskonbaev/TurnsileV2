from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from .constants import PaymentTypeChoices
from .models import PaymentType, MembershipPayment
from .serializers import PaymentTypeSerializer, PaymentTypeChoiceSerializer, MembershipPaymentSerializer
from ..accounts.models import Trainer


class PaymentTypeViewSet(ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer
    permission_classes = [AllowAny]


class MembershipPaymentViewSet(ModelViewSet):
    queryset = MembershipPayment.objects.all()
    serializer_class = MembershipPaymentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['membership', 'type']

    def perform_create(self, serializer):
        trainer_id = self.request.data.get('trainer')
        if trainer_id:
            try:
                trainer = Trainer.objects.get(id=trainer_id)
            except Trainer.DoesNotExist:
                trainer = None
        else:
            trainer = None

        serializer.save(trainer=trainer)


class PaymentTypeChoicesView(APIView):
    queryset = PaymentTypeChoices.choices
    serializer_class = PaymentTypeChoiceSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)
