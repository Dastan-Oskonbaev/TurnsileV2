from django.urls import path, include
from rest_framework import routers

from apps.journal.views import JournalViewSet

router = routers.DefaultRouter()

router.register('', JournalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
