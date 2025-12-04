from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Role, AccessRule
from .serizalizers import RoleSerializer, AccessRuleSerializer
from .permissions import HasAccess

class RoleListCreateView(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    permission_classes = [HasAccess]
    business_element_code = "roles"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_action = "read_all"
        elif self.request.method == "POST":
            self.permission_action = "create"
        return super().get_permissions()


class RoleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    permission_classes = [HasAccess]
    business_element_code = "roles"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_action = "read_all"
        elif self.request.method in ("PUT", "PATCH"):
            self.permission_action = "update_all"
        elif self.request.method == "DELETE":
            self.permission_action = "delete_all"
        return super().get_permissions()

class AccessRuleListCreateView(ListCreateAPIView):
    queryset = AccessRule.objects.select_related("role", "element").all()
    serializer_class = AccessRuleSerializer

    permission_classes = [HasAccess]
    business_element_code = "access_rules"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_action = "read_all"
        elif self.request.method == "POST":
            self.permission_action = "create"
        return super().get_permissions()


class AccessRuleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AccessRule.objects.select_related("role", "element").all()
    serializer_class = AccessRuleSerializer

    permission_classes = [HasAccess]
    business_element_code = "access_rules"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_action = "read_all"
        elif self.request.method in ("PUT", "PATCH"):
            self.permission_action = "update_all"
        elif self.request.method == "DELETE":
            self.permission_action = "delete_all"
        return super().get_permissions()

