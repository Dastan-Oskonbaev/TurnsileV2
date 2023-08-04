import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets, permissions

from utils.time import get_current_date_time
from .models import Key, ServiceCard
from .serializers import KeySerializer, ServiceCardSerializer
from .filters import KeyFilterSet

from apps.accounts.models import CustomUser


class KeyViewSet(viewsets.ModelViewSet):
    queryset = Key.objects.all()
    serializer_class = KeySerializer
    filterset_class = KeyFilterSet
    permission_classes = [permissions.IsAdminUser]


class ServiceCardViewSet(viewsets.ModelViewSet):
    queryset = ServiceCard.objects.all()
    serializer_class = ServiceCardSerializer
    permission_classes = [permissions.IsAdminUser]


class SubscriptionKeyAPIView(View):
    def post(self, request):
        messages = json.loads(request.body).get('messages')

        if not messages:
            return JsonResponse({
                'error': 1
            })

        message = messages[0]
        response_message = []

        if message.get('operation') == 'check_access':
            scan_id = message.get('card')[:12]

            key = Key.objects.filter(scan_id=scan_id).first()
            user = CustomUser.objects.filter(scan_id=scan_id).first()
            keys = Key.objects.filter(membership=user)

            channel_layer = get_channel_layer()

            if key and key.membership or keys:
                add_status_code = 423
                give_status_code = 423
            elif key or user:
                add_status_code = 409
                give_status_code = 200
            else:
                add_status_code = 200
                give_status_code = 404

            user_data = {
                'id': user.id if user else None,
                'key_id': key.id if key else None,
                'scan_id': scan_id,
            }

            message_add_key = user_data.copy()
            message_give_key = user_data.copy()

            message_add_key.update(status=add_status_code)
            message_give_key.update(status=give_status_code)

            async_to_sync(channel_layer.group_send)(
                "chat_add_scan",
                {
                    "type": "chat_message",
                    "message": message_add_key
                }
            )

            async_to_sync(channel_layer.group_send)(
                "chat_give_scan",
                {
                    "type": "chat_message",
                    "message": message_give_key
                }
            )

        elif message.get('operation') == 'events':
            length = len(message.get('events'))
            _id = message.get('id')
            response_message = [{
                'id': _id,
                'operation': 'events',
                'events_success': length
            }]

        elif message.get('operation') == 'power_on':
            _id = message.get('id')
            response_message = [{
                'id': _id,
                'operation': 'set_active',
                'active': 1,
                'online': 1
            }]

        return JsonResponse({
            'date': get_current_date_time().strftime('%d.%m.%Y %H:%M'),
            'interval': 30,
            'messages': response_message
        })
