from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "role",
        ]
        read_only_fields = [
            "id", "username", "is_active", "is_staff"
        ]
        extra_kwargs = {"role": {"required": False}}

    def validate(self, attrs):
        request = self.context.get("request")
        instance = getattr(self, "instance", None)

        if "role" in attrs:
            if not request.user.is_authenticated:
                raise serializers.ValidationError({"role": "Login required."})

            if request.user.role != User.RoleChoices.ADMIN:
                raise serializers.ValidationError({"role": "Only admin can change roles."})

        return attrs

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = self.user.role
        data["user"] = UserDetailSerializer(self.user).data
        return data
