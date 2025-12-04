from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "role",
            "is_active",
        )
        read_only_fields = ("id", "role", "is_active")

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True,)

    password = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})
    password_repeat = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})

    def validate(self, att):
        if att["password"] != att["password_repeat"]:
            raise serializers.ValidationError("Пароли не совпадают!")
        return att

    def create(self, valid_data):
        password = valid_data.pop("password")
        valid_data.pop("password_repeat", None)

        user = User.objects.create_user(password=password, **valid_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})

    def validate(self, att):
        email = att.get("email")
        password = att.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Неправильный email или пароль!")
            if not user.is_active:
                raise serializers.ValidationError("Аккаунт деактивирован!")
        else:
            raise serializers.ValidationError("Укажите email и пароль!")

        att["user"] = user
        return att


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "middle_name", "role", "is_active"]
        read_only_fields = ["id"]


class SelfUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "password",
        ]
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "middle_name": {"required": False},
            "password": {"required": False},
        }

        # def update(self, instance, validated_data):
        #     password = validated_data.pop("password", None)
        #
        #     for attr, value in validated_data.items():
        #         setattr(instance, attr, value)
        #
        #     if password:
        #         instance.set_password(password)
        #
        #     instance.save()
        #     return instance
