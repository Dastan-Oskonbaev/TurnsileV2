from django.http import JsonResponse, HttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.pool.models import Key
from utils.time import get_current_time

from .models import Journal
from .serializers import JournalSerializer
from .filters import JournalFilterSet
from .resources import JournalResource


class JournalViewSet(ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [AllowAny]
    filterset_class = JournalFilterSet

    @extend_schema(
        description='Change key of the journal entry',
        responses={200: JournalSerializer},
        request=None,
        parameters=[
            OpenApiParameter(
                name='key',
                description='Key ID',
                type=OpenApiTypes.INT,
                required=True,
                location=OpenApiParameter.QUERY
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def change_key(self, request, pk=None):
        instance = self.get_object()

        if instance.actual_exit_time:
            return JsonResponse({
                'message': 'Already exited. You cannot change the key'
            }, status=400)

        new_key = request.query_params.get('key', None)

        if not new_key:
            return JsonResponse({
                'key': 'Key is required'
            }, status=400)
        else:
            new_key = Key.objects.filter(pk=new_key).first()

            if not new_key:
                return JsonResponse({
                    'key': 'Key is not found'
                }, status=400)

            if new_key.membership:
                return JsonResponse({
                    'key': 'Key is already in use'
                }, status=400)

        instance.key.membership = None
        instance.key.save()

        instance.key = new_key
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def exit_set(self, request, pk=None):
        instance = self.get_object()

        if instance.actual_exit_time:
            return JsonResponse({
                'message': 'Already exited'
            }, status=400)

        instance.actual_exit_time = get_current_time()
        serializer = self.get_serializer(instance)

        data = serializer.data
        data["membership"] = instance.membership
        data["key"] = Key.objects.filter(pk=data.get('key')).first()

        serializer.validate(data=data)

        instance.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='export')
    def export_data(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        dataset = JournalResource().export(queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="project.xls"'
        return response
