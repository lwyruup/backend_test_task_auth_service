from typing import Optional
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from .services import check_access
from accounts.services import get_user_by_token

User = get_user_model()

def _get_user_from_request(request) -> Optional[User]:
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    token = None

    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()

    if not token:
        return None
    return get_user_by_token(token)


class HasAccess(BasePermission):
    def has_permission(self, request, view: APIView) -> bool:
        element_code: Optional[str] = getattr(view, "business_element_code", None)
        action: Optional[str] = getattr(view, "permission_action", None)

        if not element_code or not action:
            return False # будет возвращать 403

        user = _get_user_from_request(request)
        if user is None:
            return False

        return check_access(user, element_code, action, is_owner=False)

    def has_object_permission(self, request, view: APIView, obj) -> bool:
        element_code: Optional[str] = getattr(view, "business_element_code", None)
        action: Optional[str] = getattr(view, "permission_action", None)
        owner_field: str = getattr(view, "owner_field", "owner")

        if not element_code or not action:
            return False

        user = _get_user_from_request(request)
        if user is None:
            return False

        owner = getattr(obj, owner_field, None)
        is_owner = (owner == user)

        return check_access(user, element_code, action, is_owner=is_owner)