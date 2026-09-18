from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter

from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)

from .models import WorkoutPlan
from .serializers import (
    WorkoutPlanSerializer,
    WorkoutPlanBasicSerializer,
    WorkoutExerciseSerializer,
)
from rest_framework.views import APIView


class WorkoutPlanFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains")

    class Meta:
        model = WorkoutPlan
        fields = {
            "id": ["exact", "in"],
            "date_created": ["exact", "range"],
            "last_modified": ["exact", "range"],
            "name": ["exact", "icontains", "istartswith", "iendswith"],
            "day": ["exact", "in"],
            "profile": ["exact", "in"],
            "archive": [
                "exact",
                "icontains",
                "istartswith",
                "iendswith",
                "in",
                "isnull",
            ],
        }


class WorkoutPlanCreate(ListCreateAPIView):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = WorkoutPlanFilter

    ordering_fields = "__all__"
    search_fields = [
        "name",
        "day",
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


class WorkoutPlanList(ListAPIView):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanBasicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = [
        "name",
        "day",
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WorkoutPlanRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)
        return instance

    def perform_destroy(self, instance):
        instance.archive = True
        instance.updated_by = self.request.user
        instance.save()
        return instance


class WorkoutExerciseAddView(APIView):
    def post(self, request):
        serilizer = WorkoutExerciseSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        return Response({"message": "ok"})
