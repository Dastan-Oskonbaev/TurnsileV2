from django.urls import  path

from rest_framework import routers


from .views import UserViewSet, MembershipViewSet, TrainerViewSet, TrainerScheduleViewSet

router = routers.DefaultRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'membership', MembershipViewSet, basename='membership')
router.register(r'trainer', TrainerViewSet, basename='trainer')
router.register(r'trainer-schedule', TrainerScheduleViewSet, basename='trainer-schedule')

urlpatterns = router.urls
