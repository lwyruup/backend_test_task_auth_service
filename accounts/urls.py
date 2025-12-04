from django.urls import path
from .views import LoginView, RegisterView, MeView, UserListView, AdminUserDetailView, AdminUserListCreateView, LogoutView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="auth-me-please"),
    # path("users/", UserListView.as_view(), name="user-list"),
    path("users/", AdminUserListCreateView.as_view(), name="admin-user-list"),
    path("users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail")
]

