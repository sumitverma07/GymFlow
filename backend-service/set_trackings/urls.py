from django.urls import path

from .views import (
    SetTrackingCreate,
    SetTrackingRetrieveUpdateDestroyAPI,
    SetTrackingList,
    SetTrackingView,
)

urlpatterns = [
    path("", SetTrackingCreate.as_view()),
    path("all/", SetTrackingList.as_view()),
    path("<int:pk>/", SetTrackingRetrieveUpdateDestroyAPI.as_view()),
    path("create/", SetTrackingView.as_view()),
]
