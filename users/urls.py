from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("update/",
         views.UserChange.as_view(), name="user_update"),
    path("profile/<int:pk>/",
         views.UserProfileView.as_view(), name="user_profile"),
]
