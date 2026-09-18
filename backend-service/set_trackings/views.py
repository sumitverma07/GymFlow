from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter

from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)

from .models import SetTracking
from .serializers import (
    SetTrackingSerializer,
    SetTrackingBasicSerializer,
    RecordSetSerializer,
)


class SetTrackingFilter(FilterSet):

    class Meta:
        model = SetTracking
        fields = {
            "id": ["exact", "in"],
            "date_created": ["exact", "range"],
            "last_modified": ["exact", "range"],
            "set_number": ["exact", "in", "gte", "lte"],
            "reps": ["exact", "in", "gte", "lte"],
            "weight": ["exact", "in", "gte", "lte"],
            "performed_workout_id": ["exact", "in"],
            "exercise_id": ["exact", "in"],
            "archive": ["exact", "in", "isnull"],
        }


class SetTrackingCreate(ListCreateAPIView):
    queryset = SetTracking.objects.all()
    serializer_class = SetTrackingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = SetTrackingFilter

    ordering_fields = "__all__"
    search_fields = [
        "set_number",
        "reps",
        "weight",
    ]

    def perform_create(self, serializer):
        instance = serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SetTrackingList(ListAPIView):
    queryset = SetTracking.objects.all()
    serializer_class = SetTrackingBasicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = [
        "set_number",
        "reps",
        "weight",
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SetTrackingRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = SetTracking.objects.all()
    serializer_class = SetTrackingSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)
        return instance

    def perform_destroy(self, instance):
        instance.archive = True
        instance.updated_by = self.request.user
        instance.save()
        return instance


class SetTrackingView(APIView):
    def post(self, request):
        serializer = RecordSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Created Successfully"})
