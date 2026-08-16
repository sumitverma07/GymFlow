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

from .models import Profile
from .serializers import (
    ProfileSerializer,
    ProfileBasicSerializer,
)

class ProfileFilter(FilterSet):
    phone_no = CharFilter(lookup_expr='icontains')
    address = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = {
            'id': ['exact', 'in'],
            'date_created':['exact', 'range'],
            'last_modified':['exact', 'range'],
            'phone_no': ['exact', 'icontains', 'istartswith', 'iendswith'],
            'address': ['exact', 'icontains', 'istartswith', 'iendswith'],
            'archive': ['exact', 'icontains', 'istartswith', 'iendswith', 'in', 'isnull'],
        }


class ProfileCreate(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = ProfileFilter

    ordering_fields = '__all__'
    search_fields = [
        'phone_no',
        'address',
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

    
class ProfileList(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileBasicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter, 
        filters.OrderingFilter, 
        DjangoFilterBackend
    ]
    filter_fields = '__all__'
    ordering_fields = '__all__'
    search_fields = [
        'phone_no',
        'address',
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
        instance = serializer.save(
            updated_by=self.request.user
        )
        return instance
    def perform_destroy(self, instance):
        instance.archive = True
        instance.updated_by = self.request.user
        instance.save()
        return instance