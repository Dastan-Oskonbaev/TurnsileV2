from django.urls import path

from .views import TurnstileHistoryView, TurnstileHistoryView2

urlpatterns = [
    path('', TurnstileHistoryView.as_view(), name='turnstile_history'),
    path('second/', TurnstileHistoryView2.as_view(), name='turnstile_history2'),
]
