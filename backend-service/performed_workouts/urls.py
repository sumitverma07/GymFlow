from django.urls import path

from .views import (
    PerformedWorkoutCreate,
    PerformedWorkoutRetrieveUpdateDestroyAPI,
    PerformedWorkoutList,
    PerformedWorkoutDetailView,
)

urlpatterns = [
    path("", PerformedWorkoutCreate.as_view()),
    path("all/", PerformedWorkoutList.as_view()),
    path("<int:pk>/", PerformedWorkoutRetrieveUpdateDestroyAPI.as_view()),
    path("get/<int:pk>/", PerformedWorkoutDetailView.as_view()),
]
