from django.urls import path

from .views import (
    ProfileCreate,
    ProfileRetrieveUpdateDestroyAPI,
    ProfileList,
)

urlpatterns = [
    path('', ProfileCreate.as_view()),
    path('all/', ProfileList.as_view()),
    path('<int:pk>/', ProfileRetrieveUpdateDestroyAPI.as_view()),
]