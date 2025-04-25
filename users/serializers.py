from rest_framework import serializers
from users.models import CustomUser, VerificationCode, UserData
import random


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Неверный формат номера телефона")
        return value

    def save(self):
        phone_number = self.validated_data["phone_number"]
        user, created = CustomUser.objects.get_or_create(
            phone=phone_number, username=phone_number
        )
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])  # Генерация кода
        VerificationCode.objects.create(user=user, code=code)
        # Здесь должна быть логика отправки SMS (например, через Twilio)
        print(f"SMS code for {phone_number}: {code}")  # Для теста выводим в консоль
        return code


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get("phone_number")
        code = data.get("code")
        try:
            user = CustomUser.objects.get(phone=phone_number)
            verification = VerificationCode.objects.filter(
                user=user, code=code, is_used=False
            ).latest("created_at")
        except (CustomUser.DoesNotExist, VerificationCode.DoesNotExist):
            raise serializers.ValidationError("Неверный номер телефона или код")
        data["user"] = user
        data["verification"] = verification
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(read_only=True, source="userdata.gender")
    age = serializers.IntegerField(read_only=False, source="userdata.age")
    birthday = serializers.DateTimeField(read_only=False, source="userdata.birthday")
    city = serializers.CharField(read_only=False, source="userdata.city")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "gender",
            "age",
            "birthday",
            "city",
        ]


class UpdateCustomUserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    gender = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    birthday = serializers.DateTimeField(required=True)
    city = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "gender",
            "age",
            "birthday",
            "city",
        ]

    def validate_age(self, value: int) -> int | None:
        # print(self.context["view"].kwargs.get("pk"))
        if value and value >= 0:
            return value
        if value and value < 0:
            raise serializers.ValidationError("Age can't lower zero")
        return 0

    def validate_gender(self, value: str) -> str:
        if value.upper() in UserData.GenderType:
            return value.upper()
        raise serializers.ValidationError("Invalid gender")

    def update(self, instance: CustomUser, validated_data):
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")
        instance.middle_name = validated_data.get("middle_name")
        instance.email = validated_data.get("email")
        if getattr(instance, "userdata", None):
            instance.userdata.gender = validated_data.get("gender")
            instance.userdata.age = validated_data.get("age")
            instance.userdata.birthday = validated_data.get("birthday")
            instance.userdata.city = validated_data.get("city")
            instance.save()
        else:
            UserData.objects.create(
                user=instance,
                gender=validated_data.get("gender"),
                age=validated_data.get("age"),
                birthday=validated_data.get("birthday"),
                city=validated_data.get("city"),
            )
