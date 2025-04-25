from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics, mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from .serializers import (
    PhoneNumberSerializer,
    VerifyCodeSerializer,
    CustomUserSerializer,
    UpdateCustomUserSerializer,
)


class RequestCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.save()
            return Response(
                {"message": "Код отправлен", "code": code}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            verification = serializer.validated_data["verification"]
            verification.is_used = True  # Помечаем код как использованный
            verification.save()

            # Генерируем refresh и access токены для пользователя
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Успешный вход",
                    "refresh": str(refresh),  # Refresh-токен
                    "access": str(refresh.access_token),  # Access-токен
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CustomUserSerializer
        if self.request.method in ["PUT"]:
            return UpdateCustomUserSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        custom_user = (
            CustomUser.objects.select_related("userdata")
            .filter(id=kwargs["pk"])
            .first()
        )
        if not custom_user:
            return Response(
                {"error": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if serializer.is_valid():
            serializer.update(custom_user, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateCustomUserSerializer()
    queryset = CustomUser.objects.all()
