from django.urls import path

from .views import (
    ProfileCreate,
    ProfileRetrieveUpdateDestroyAPI,
    ProfileList,
    RegisterUserView,
    VerifyCodeView,
    LoginView,
)

urlpatterns = [
    path("", ProfileCreate.as_view()),
    path("all/", ProfileList.as_view()),
    path("<int:pk>/", ProfileRetrieveUpdateDestroyAPI.as_view()),
    path("register/", RegisterUserView.as_view()),
    path("verify/", VerifyCodeView.as_view()),
    path("login/", LoginView.as_view()),
]
