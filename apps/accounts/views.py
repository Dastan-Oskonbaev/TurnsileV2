from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django_filters import rest_framework as filters

from apps.history.models import MembershipHistory, HistoryType
from apps.history.serializers import MembershipHistorySerializer
from apps.history.constants import HistoryTypeChoices
from .constants import RoleChoices
from .filters import MembershipFilter

from .models import CustomUser, Membership, Trainer, TrainerSchedule
from .serializers import (
    UserSerializer,
    MembershipSerializer,
    TrainerSerializer,
    TrainerScheduleSerializer,
    UserChangePasswordSerializer,
    TrainerUpdateSerializer,
    UserUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(role__in=[RoleChoices.OWNER, RoleChoices.ADMIN])
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user

        if user.is_anonymous:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = self.get_serializer(user)

        return Response(serializer.data)

    @extend_schema(request=UserChangePasswordSerializer)
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user

        if user.is_anonymous:
            return Response({'detail': 'Not found.'}, status=404)

        password = request.data.get('password')
        new_password = request.data.get('new_password')

        if not check_password(password, user.password):
            return Response({'error': _('Invalid password.')}, status=400)

        if new_password:
            user.password = new_password
            user.save()

            return Response({'success': 'Password changed successfully.'})
        else:
            return Response({'error': 'New password not provided.'}, status=400)


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    filterset_class = MembershipFilter

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user

        if user.is_anonymous:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = self.get_serializer(user)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        history = self.get_object().history.all()
        serializer = MembershipHistorySerializer(history, many=True)
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def freeze(self, request, pk=None):
        freeze_days = request.data.get('days', None)

        if not freeze_days:
            return Response({
                'error': _('Freeze days not found!')
            })

        membership = self.get_object()

        payment = membership.get_actual_payment()

        if not payment:
            return Response({
                'error': _('Payment not found!')
            })

        payment.end_date += timedelta(days=freeze_days)
        payment.is_active = False
        payment.save()

        history_type = HistoryType.objects.get_or_create(
            name=HistoryTypeChoices.FREEZE
        )[0]

        MembershipHistory.objects.create(
            membership=membership,
            type=history_type,
            description=_("Заморозка на") + f" {freeze_days}" + _("дней")
        )

        return Response({
            'success': _('Membership frozen!')
        })

    @action(detail=True, methods=['get'])
    def unfreeze(self, request, pk=None):
        membership = self.get_object()

        payment = membership.get_freeze_payment()

        if not payment:
            return Response({
                'error': _('Payment not found!')
            })

        payment.is_active = True
        payment.save()

        history_type = HistoryType.objects.get_or_create(
            name=HistoryTypeChoices.UNFREEZE
        )[0]

        MembershipHistory.objects.create(
            membership=membership,
            type=history_type,
            description=_("Разморозка")
        )

        return Response({
            'success': _('Membership unfrozen!')
        })

    @transaction.atomic
    @action(detail=True, methods=['get'])
    def refund(self, request, pk=None):
        membership = self.get_object()

        payment = membership.get_actual_payment()

        if not payment:
            return Response({
                'error': _('Payment not found!')
            })

        refund_sum = payment.amount - (
                payment.amount / payment.visits_count * (payment.visits_count - membership.remaining_visits)
        )

        history_type = HistoryType.objects.get_or_create(
            name=HistoryTypeChoices.REFUND
        )[0]

        MembershipHistory.objects.create(
            membership=membership,
            type=history_type,
            description=_("Возврат суммы в размере") + f" {refund_sum}"
        )

        membership.remaining_visits = 0
        membership.save()

        payment.is_active = False
        payment.save()

        return Response({
            'success': _('Refund success!'),
            'refund_sum': refund_sum
        })


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search', '')

        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'update':
            return TrainerUpdateSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user

        if user.is_anonymous:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = self.get_serializer(user)

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request, pk=None):
        trainer = request.user
        password = request.data.get('password')
        new_password = request.data.get('new_password')

        if not check_password(password, trainer.password):
            return Response({'error': _('Invalid password.')}, status=400)

        if new_password:
            trainer.password = new_password
            trainer.save()

            return Response({'success': 'Password changed successfully.'})
        else:
            return Response({'error': 'New password not provided.'}, status=400)


class TrainerScheduleViewSet(viewsets.ModelViewSet):
    queryset = TrainerSchedule.objects.all()
    serializer_class = TrainerScheduleSerializer
