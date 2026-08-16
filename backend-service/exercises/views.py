from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import (
    FilterSet,
    CharFilter
)

from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView, 
    ListAPIView,
)

from .models import Exercise
from .serializers import (
    ExerciseSerializer,
    ExerciseBasicSerializer,
)

class ExerciseFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    muscle_group = CharFilter(lookup_expr='icontains')
    instructions = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Exercise
        fields = {
            'id': ['exact', 'in'],
            'date_created':['exact', 'range'],
            'last_modified':['exact', 'range'],
            'name': ['exact', 'icontains', 'istartswith', 'iendswith'],
            'category': ['exact', 'in', 'isnull'],
            'muscle_group': ['exact', 'icontains', 'istartswith', 'iendswith', 'in'],
            'instructions': ['exact', 'icontains', 'istartswith', 'iendswith'],
            'archive': ['exact', 'icontains', 'istartswith', 'iendswith', 'in', 'isnull'],
        }


class ExerciseCreate(ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = ExerciseFilter

    ordering_fields = '__all__'
    search_fields = [
        'name',
        'muscle_group',
        'instructions',
    ]

    def perform_create(self, serializer):
        instance = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
class ExerciseList(ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseBasicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter, 
        filters.OrderingFilter, 
        DjangoFilterBackend
    ]
    filter_fields = '__all__'
    ordering_fields = '__all__'
    search_fields = [
        'name',
        'muscle_group',
        'instructions',
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ExerciseRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        instance = serializer.save(
            updated_by=self.request.user
        )
        return instance
        
    def perform_destroy(self, instance):
        instance.archive = True
        instance.updated_by = self.request.user
        instance.save()
        return instance