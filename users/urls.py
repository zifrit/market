from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import RequestCodeView, VerifyCodeView, UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("auth/request-code/", RequestCodeView.as_view(), name="request_code"),
    path("auth/verify-code/", VerifyCodeView.as_view(), name="verify_code"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
