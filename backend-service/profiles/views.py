from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter

from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)

from .models import Profile
from .serializers import (
    ProfileSerializer,
    ProfileBasicSerializer,
    UserSerializer,
    VerifyCodeSerializer,
    LoginSerializer,
)
from gymflow.utils import send_verification_email, generate_verification_code
from rest_framework_simplejwt.tokens import RefreshToken

OTP_TTL_SECONDS = 10 * 60


class ProfileFilter(FilterSet):
    phone_no = CharFilter(lookup_expr="icontains")
    address = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Profile
        fields = {
            "id": ["exact", "in"],
            "date_created": ["exact", "range"],
            "last_modified": ["exact", "range"],
            "phone_no": ["exact", "icontains", "istartswith", "iendswith"],
            "address": ["exact", "icontains", "istartswith", "iendswith"],
            "archive": [
                "exact",
                "icontains",
                "istartswith",
                "iendswith",
                "in",
                "isnull",
            ],
        }


class ProfileCreate(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = ProfileFilter

    ordering_fields = "__all__"
    search_fields = [
        "phone_no",
        "address",
    ]

    def perform_create(self, serializer):
        instance = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfileList(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileBasicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = [
        "phone_no",
        "address",
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfileRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)
        return instance

    def perform_destroy(self, instance):
        instance.archive = True
        instance.updated_by = self.request.user
        instance.save()
        return instance


def _cache_key(email):
    return f"signup_otp:{email.lower()}"


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # email = serializer.validated_data["email"]
        # password = serializer.validated_data["password"]

        # code = generate_verification_code()
        # cache.set(
        #     _cache_key(email),  # key — must be a string
        #     {
        #         "password_hash": make_password(password),
        #         "otp": code,
        #     },
        #     timeout=OTP_TTL_SECONDS,  # expiry in seconds
        # )

        # send_verification_email(email, code)
        # print("code is ", code)
        return Response(
            {
                "detail": "We've sent a verification code to your email. Please enter it to complete signup."
            }
        )


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # email = serializer.validated_data["email"]
        # code = serializer.validated_data["code"]
        # key = _cache_key(email)
        # pending = cache.get(key)

        # password = pending["password_hash"]
        # if pending["otp"] != code:
        #     return Response({"detail": "Invalid code."})
        # user = User.objects.create(
        #     username=email,
        #     email=email,
        # )
        # user.set_password(password)
        # Profile.objects.create(user=user)
        # cache.delete(key)
        return Response({"detail": "Account created successfully."})


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh_token = RefreshToken.for_user(user)
        return Response(
            {
                "accessToken": str(refresh_token.access_token),
                "refreshToken": str(refresh_token),
            },
        )
