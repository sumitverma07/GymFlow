from django.urls import path

from .views import (
    WorkoutPlanCreate,
    WorkoutPlanRetrieveUpdateDestroyAPI,
    WorkoutPlanList,
    WorkoutExerciseAddView,
)

urlpatterns = [
    path("", WorkoutPlanCreate.as_view()),
    path("all/", WorkoutPlanList.as_view()),
    path("<int:pk>/", WorkoutPlanRetrieveUpdateDestroyAPI.as_view()),
    path("add/", WorkoutExerciseAddView.as_view()),
]
