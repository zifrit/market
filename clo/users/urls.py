from django.urls import path
from users.views import RequestCodeView, VerifyCodeView

urlpatterns = [
    path('auth/request-code/', RequestCodeView.as_view(), name='request_code'),
    path('auth/verify-code/', VerifyCodeView.as_view(), name='verify_code'),
]