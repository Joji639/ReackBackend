
from rest_framework import serializers
from .models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


class SignUpSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)  

    class Meta:
        model = UserModel
        fields = ["id", "username", "email", "password", "confirmPassword"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        if data["password"] != data["confirmPassword"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirmPassword")
        password = validated_data.pop("password")
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = UserModel.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email,
            "name": user.username,
            "role": user.role,
        }

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    uid = serializers.CharField()  
    token = serializers.CharField()

    def validate(self, data):
        
        if data["password"] != data["confirmPassword"]:
            raise serializers.ValidationError("Passwords do not match")

        
        try:
            uid = force_str(urlsafe_base64_decode(data["uid"])) #encoded id
            user = UserModel.objects.get(id=uid)
        except Exception:
            raise serializers.ValidationError("Invalid user")

        
        if not PasswordResetTokenGenerator().check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid or expired token")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        password = self.validated_data["password"]

        user.set_password(password)
        user.save()

        return user
