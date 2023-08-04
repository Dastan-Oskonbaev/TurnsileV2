from django.urls import include, path
from rest_framework import routers

from apps.payments.views import PaymentTypeViewSet, MembershipPaymentViewSet, PaymentTypeChoicesView

router = routers.DefaultRouter()

router.register('types', PaymentTypeViewSet)
router.register('membership', MembershipPaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('type-choices/', PaymentTypeChoicesView.as_view()),
]