from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from django.db.models import Prefetch

from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)

from .models import PerformedWorkout
from .serializers import (
    PerformedWorkoutSerializer,
    PerformedWorkoutBasicSerializer,
    PerformedWorkoutDetailSerializer,
)
from django.db import connection
from set_trackings.models import SetTracking


class PerformedWorkoutFilter(FilterSet):
    notes = CharFilter(lookup_expr="icontains")

    class Meta:
        model = PerformedWorkout
        fields = {
            "id": ["exact", "in"],
            "date_created": ["exact", "range"],
            "last_modified": ["exact", "range"],
            "performed_at": ["exact", "range"],
            "profile": ["exact", "in"],
            "notes": ["exact", "icontains", "istartswith", "iendswith"],
            "archive": [
                "exact",
                "icontains",
                "istartswith",
                "iendswith",
                "in",
                "isnull",
            ],
        }


class PerformedWorkoutCreate(ListCreateAPIView):
    queryset = PerformedWorkout.objects.all()
    serializer_class = PerformedWorkoutSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = PerformedWorkoutFilter

    ordering_fields = "__all__"
    search_fields = [
        "notes",
    ]

    def perform_create(self, serializer):
        instance = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            profile=self.request.user.profile,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PerformedWorkoutList(ListAPIView):
    serializer_class = PerformedWorkoutBasicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = ["notes"]

    def get_queryset(self):
        user_profile_id = self.request.user.profile.id
        return (
            PerformedWorkout.objects.select_related("workout_plan")
            .filter(profile_id=user_profile_id)
            .order_by("id")
        )


class PerformedWorkoutRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = PerformedWorkout.objects.all()
    serializer_class = PerformedWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)
        return instance

    def perform_destroy(self, instance):
        instance.archive = True
        instance.updated_by = self.request.user
        instance.save()
        return instance


class PerformedWorkoutDetailView(APIView):
    def get(self, request, pk):
        try:
            pw = PerformedWorkout.objects.prefetch_related(
                Prefetch(
                    "set_tracking_performed_workout",
                    queryset=SetTracking.objects.select_related("exercise"),
                    to_attr="set_trackings",
                )
            ).get(id=pk)
        except PerformedWorkout.DoesNotExist:
            return Response({"message": "Not Found id"})
        serializer = PerformedWorkoutDetailSerializer(pw)

        res = serializer.data
        return Response(res)
