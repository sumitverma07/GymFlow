from django.urls import path

from .views import (
    ExerciseCreate,
    ExerciseRetrieveUpdateDestroyAPI,
    ExerciseList,
)

urlpatterns = [
    path('', ExerciseCreate.as_view()),
    path('all/', ExerciseList.as_view()),
    path('<int:pk>/', ExerciseRetrieveUpdateDestroyAPI.as_view()),
]