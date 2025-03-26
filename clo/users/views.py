from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import PhoneNumberSerializer, VerifyCodeSerializer

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