from django.urls import path
from .views import RoleDetailView, RoleListCreateView, AccessRuleListCreateView, AccessRuleDetailView

urlpatterns = [
    path("roles/", RoleListCreateView.as_view(), name="role-list"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-details"),
    path("access-rules/", AccessRuleListCreateView.as_view(), name="access-rules-list"),
    path("access-rules/<int:pk>/", AccessRuleDetailView.as_view(), name="access-rule-detail")



]