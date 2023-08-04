from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HistoryTypeViewSet

router = DefaultRouter()

router.register('types', HistoryTypeViewSet)

urlpatterns = router.urls
