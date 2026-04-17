from rest_framework import serializers
from .models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


# ================= SIGNUP =================
class SignUpSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["id", "username", "email", "password", "confirmPassword"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        try:
            if data["password"] != data["confirmPassword"]:
                raise serializers.ValidationError("Passwords do not match")
            return data
        except Exception:
            raise serializers.ValidationError("Validation failed")

    def create(self, validated_data):
        try:
            validated_data.pop("confirmPassword")
            password = validated_data.pop("password")

            # ✅ Use create_user (best practice)
            user = UserModel.objects.create_user(
                password=password,
                **validated_data
            )

            return user
        except Exception:
            raise serializers.ValidationError("User creation failed")


# ================= LOGIN =================
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            email = data.get("email")
            password = data.get("password")

            user = UserModel.objects.filter(email=email).first()

            if user is None or not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials")

            if user.status == "blocked":
                raise serializers.ValidationError("Your account is blocked by admin")

            refresh = RefreshToken.for_user(user)

            # ✅ FIX: Proper admin detection
            role = "admin" if user.is_superuser else user.role

            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "email": user.email,
                "name": user.username,
                "role": role,
            }

        except serializers.ValidationError as e:
            raise e
        except Exception:
            raise serializers.ValidationError("Login failed")


# ================= RESET PASSWORD =================
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            # 🔹 Password match check
            if data["password"] != data["confirmPassword"]:
                raise serializers.ValidationError("Passwords do not match")

            # 🔹 Decode user
            uid = force_str(urlsafe_base64_decode(data["uid"]))
            user = UserModel.objects.get(id=uid)

            # 🔹 Token check
            if not PasswordResetTokenGenerator().check_token(user, data["token"]):
                raise serializers.ValidationError("Invalid or expired token")

            data["user"] = user
            return data

        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User not found")
        except Exception:
            raise serializers.ValidationError("Invalid reset request")

    def save(self):
        try:
            user = self.validated_data["user"]
            password = self.validated_data["password"]

            user.set_password(password)
            user.save()

            return user
        except Exception:
            raise serializers.ValidationError("Password reset failed")