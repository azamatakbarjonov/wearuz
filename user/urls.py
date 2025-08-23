from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("edit/", views.edit_profile, name="edit_profile"),
    # user akk ochganini korish uchun all users
    path("all-users/", views.all_users, name="all_users"),
]
