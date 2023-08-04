import json

from django.http import JsonResponse
from django.views import View

from apps.pool.models import Key, ServiceCard
from apps.turnstile.models import TurnstileHistory
from utils.time import get_current_date_time


class TurnstileHistoryView(View):
    def post(self, request):
        messages = json.loads(request.body).get('messages')

        if not messages:
            return JsonResponse({
                'error': 1
            }, status=404)

        message = messages[0]
        response_messages = []

        operation = message.get('operation', '')
        _id = message.get('id')

        if operation == 'check_access':
            scan_id = message.get('card')[:12]
            reader = message.get('reader')

            state = True if reader == 1 else False
            granted = 0

            key = Key.objects.filter(scan_id=scan_id).first()
            service_card = ServiceCard.objects.filter(scan_id=scan_id).first()

            if key and key.membership:
                TurnstileHistory.objects.create(key=key, membership=key.membership, status=state)
                granted = 1
            elif service_card:
                TurnstileHistory.objects.create(service_card=service_card, status=state)
                granted = 1

            response_messages.append({
                'id': _id,
                'operation': 'check_access',
                'granted': granted
            })
        elif operation == 'power_on':
            response_messages.append({
                'id': _id,
                'operation': 'set_active',
                'active': 1,
                'online': 1
            })
        elif operation == 'events':
            length = len(message.get('events'))
            response_messages.append({
                'id': _id,
                'operation': 'events',
                'events_success': length
            })

        return JsonResponse({
            'date': get_current_date_time().strftime('%d.%m.%Y %H:%M'),
            'interval': 2,
            'messages': response_messages
        })


class TurnstileHistoryView2(View):
    def post(self, request):
        message = json.loads(request.body)

        key = message.get('card')
        reader = message.get('reader')

        state = True if reader == 1 else False
        granted = 0

        key = Key.objects.filter(scan_id=key).first() or ServiceCard.objects.filter(scan_id=key).first()

        if key and key.subscription:
            TurnstileHistory.objects.create(key=key.scan_id, subscription=key.subscription, state=state)
            granted = 1
        elif key:
            TurnstileHistory.objects.create(key=key.scan_id, state=state)

        return JsonResponse({
            'granted': granted,
            'duration': 3  # TODO: будет браться с настроек
        })
