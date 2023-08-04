from django.urls import path, include
from rest_framework import routers

from .views import KeyViewSet, ServiceCardViewSet, SubscriptionKeyAPIView

router = routers.DefaultRouter()

router.register(r'keys', KeyViewSet)
router.register(r'service-cards', ServiceCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subscription-key/', SubscriptionKeyAPIView.as_view()),
]
