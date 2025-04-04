from django.urls import path, include
from users.views import RequestCodeView, VerifyCodeView, UserViewSet
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/request-code/', RequestCodeView.as_view(), name='request_code'),
    path('auth/verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('', include(router.urls)),
]