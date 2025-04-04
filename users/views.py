from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics, mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from .serializers import PhoneNumberSerializer, VerifyCodeSerializer, CustomUserSerializer

class RequestCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Код отправлен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            verification = serializer.validated_data['verification']
            verification.is_used = True  # Помечаем код как использованный
            verification.save()

            # Генерируем refresh и access токены для пользователя
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Успешный вход",
                "refresh": str(refresh),           # Refresh-токен
                "access": str(refresh.access_token) # Access-токен
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer