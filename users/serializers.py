from rest_framework import serializers
from users.models import CustomUser, VerificationCode
import random

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Неверный формат номера телефона")
        return value

    def save(self):
        phone_number = self.validated_data['phone_number']
        user, created = CustomUser.objects.get_or_create(phone=phone_number)
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Генерация кода
        VerificationCode.objects.create(user=user, code=code)
        # Здесь должна быть логика отправки SMS (например, через Twilio)
        print(f"SMS code for {phone_number}: {code}")  # Для теста выводим в консоль
        return user

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        code = data.get('code')
        try:
            user = CustomUser.objects.get(phone=phone_number)
            verification = VerificationCode.objects.filter(user=user, code=code, is_used=False).latest('created_at')
        except (CustomUser.DoesNotExist, VerificationCode.DoesNotExist):
            raise serializers.ValidationError("Неверный номер телефона или код")
        data['user'] = user
        data['verification'] = verification
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')