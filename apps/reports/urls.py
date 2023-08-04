from django.urls import path

from apps.reports.views import ReportAPIView

urlpatterns = [
    path('report/', ReportAPIView.as_view()),
]
