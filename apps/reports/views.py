from collections import defaultdict
from datetime import datetime
from itertools import chain

from django.db.models import Sum, Count, F, Q
from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from utils.time import generate_dates
from apps.payments.models import MembershipPayment
from apps.payments.constants import PaymentTypeChoices
from apps.journal.models import Journal

from .serializers import ReportSerializer, SalesSerializer


class ReportAPIView(APIView):
    queryset = MembershipPayment.objects.none()
    serializer_class = ReportSerializer

    @extend_schema(
        description='Get report data',
        parameters=[
            OpenApiParameter(
                name='start_date',
                description='Start date',
                required=True,
                type=str,
                location='query',
                default=datetime.now().strftime('%Y-%m-%d'),
            ),
            OpenApiParameter(
                name='end_date',
                description='End date',
                required=True,
                type=str,
                location='query',
                default=datetime.now().strftime('%Y-%m-%d'),
            ),
        ],
        responses={
            200: {
                'report': {},
                'sales': [],
                'dates': [],
            },
            400: 'Bad request',
        },
    )
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({
                'error': _("start and end_date are required parameters")
            }, status=400)

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        dates = generate_dates(start_date, end_date)

        membership_filter = Q(created_at__date__range=(start_date, end_date), type__type=PaymentTypeChoices.MEMBERSHIP)

        membership_total_income = MembershipPayment.objects.filter(
            membership_filter
        ).aggregate(
            total_income=Sum('amount')
        ).get('total_income', 0)

        one_time_income = Journal.objects.filter(
            create_date__in=dates,
            payment__type__type=PaymentTypeChoices.ONE_TIME
        ).values('payment__id').annotate(
            total_income=Sum('payment__amount')
        ).aggregate(
            total_income_sum=Sum('total_income')
        ).get('total_income_sum', 0)

        membership_total_income = membership_total_income if membership_total_income else 0
        one_time_income = one_time_income if one_time_income else 0

        total_income = membership_total_income + one_time_income

        active_and_new_memberships = MembershipPayment.objects.filter(
            start_date__in=dates,
            type__type=PaymentTypeChoices.MEMBERSHIP
        ).aggregate(
            active_memberships=Count('pk', filter=Q(is_active=True)),
            new_memberships=Count('pk', filter=Q(start_date__in=dates))
        )

        one_time_visits = Journal.objects.filter(
            create_date__in=dates,
            payment__type__type=PaymentTypeChoices.ONE_TIME
        ).count()

        report_data = {
            'total_income': total_income,
            'active_memberships': active_and_new_memberships.get('active_memberships', 0),
            'new_memberships': active_and_new_memberships.get('new_memberships', 0),
            'one_time_visits': one_time_visits,
        }

        sales_membership = MembershipPayment.objects.filter(
            membership_filter
        ).values(
            name=F('type__name'),
        ).annotate(
            count=Count('type'),
            amount=Sum('amount')
        )

        sales_one_time = Journal.objects.filter(
            create_date__in=dates,
            payment__type__type=PaymentTypeChoices.ONE_TIME
        ).values(
            name=F('membership_type__name')
        ).annotate(
            count=Count('payment__type'),
            amount=Sum('payment__amount')
        )

        combined_sales = list(chain(sales_membership, sales_one_time))

        sales_serializer = SalesSerializer(combined_sales, many=True)
        sales_data = sales_serializer.data

        total_amount = sum(item['amount'] for item in sales_data)

        for item in sales_data:
            percentage = (item['amount'] / total_amount) * 100
            item['percentage'] = '{:.2f}'.format(percentage)

        dates_membership = MembershipPayment.objects.filter(
            membership_filter
        ).values(
            date=F('created_at__date'),
            name=F('type__name')
        ).annotate(
            count=Count('pk')
        ).order_by(
            'created_at__date'
        ).distinct()

        dates_one_time = Journal.objects.filter(
            create_date__in=dates,
            payment__type__type=PaymentTypeChoices.ONE_TIME
        ).values(
            date=F('create_date'),
            name=F('membership_type__name')
        ).annotate(
            count=Count('pk')
        ).order_by(
            'create_date'
        ).distinct()

        # Преобразование данных dates_membership в желаемую структуру словаря
        dates_membership_dict = defaultdict(list)
        for item in dates_membership:
            name = item['name']
            date = item['date'].strftime('%Y-%m-%d')
            count = item['count']

            # Дополнительный запрос для получения суммы (amount)
            amount = MembershipPayment.objects.filter(
                created_at__date=item['date'],
                type__name=item['name']
            ).aggregate(total_amount=Sum('amount')).get('total_amount', 0)

            dates_membership_dict[name].append({'date': date, 'count': count, 'amount': amount})

        # Преобразование данных dates_one_time в желаемую структуру словаря
        dates_one_time_dict = defaultdict(list)
        for item in dates_one_time:
            name = item['name']
            date = item['date'].strftime('%Y-%m-%d')
            count = item['count']

            # Дополнительный запрос для получения суммы (amount)
            amount = Journal.objects.filter(
                create_date=item['date'],
                membership_type__name=item['name']
            ).aggregate(total_amount=Sum('payment__amount')).get('total_amount', 0)

            dates_one_time_dict[name].append({'date': date, 'count': count, 'amount': amount})

        dates = []

        for name, items in dates_membership_dict.items():
            dates.append({'name': name, 'values': items})

        for name, items in dates_one_time_dict.items():
            dates.append({'name': name, 'values': items})

        report_serializer = ReportSerializer(report_data)

        return Response({
            'report': report_serializer.data,
            'sales': sales_serializer.data,
            'dates': dates
        })
