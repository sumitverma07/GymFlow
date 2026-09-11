from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.cache import cache
from .models import Profile
from gymflow.utils import send_verification_email, generate_verification_code

OTP_TTL_SECONDS = 10 * 60


def _cache_key(email):
    return f"signup_otp:{email.lower()}"


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "phone_no",
        ]


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        code = generate_verification_code()
        self._cache_pending_signup(email, password, code)
        send_verification_email(email, code)

        return validated_data

    def _cache_pending_signup(self, email, password, code):
        cache.set(
            _cache_key(email),  # key — must be a string
            {
                "password": password,
                "otp": code,
            },
            timeout=OTP_TTL_SECONDS,  # expiry in seconds
        )


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        key = _cache_key(email)
        pending = cache.get(key)
        if pending is None:
            raise serializers.ValidationError(
                {"detail": "Code expired or not requested. Please request a new one."}
            )
        if pending["otp"] != code:
            raise serializers.ValidationError({"detail": "Invalid code."})
        attrs["pending"] = pending
        return super().validate(attrs)

    def create(self, validated_data):
        email = validated_data.get("email")
        pending = validated_data.get("pending")
        user = User.objects.create(
            username=email,
            email=email,
        )

        user.set_password(pending["password"])
        user.save()

        Profile.objects.create(user=user)
        cache.delete(_cache_key(email))
        return validated_data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        print(email, password)
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                {"message": "Invalid email or password sumit"}
            )
        attrs["user"] = user
        print(attrs)
        return super().validate(attrs)
