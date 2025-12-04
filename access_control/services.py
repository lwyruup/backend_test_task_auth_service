from typing import Optional
from django.contrib.auth import get_user_model
from .models import (BussinessElement, AccessRule)

User = get_user_model()

def get_rule_for(user: User, element_code: str) -> Optional[AccessRule]:
    if not user.is_authenticated:
        return None
    if user.role is None:
        return None
    try:
        return AccessRule.objects.select_related("role", "element").get(role=user.role, element__code=element_code,)
    except AccessRule.DoesNotExist:
        return None

def check_access(user:User, element_code: str, action: str, is_owner: bool) -> bool:
    if not user.is_authenticated:
        return False

    rule = get_rule_for(user, element_code)
    if rule is None:
        return False

    # для action
    field_map = {
        "read": "read_permission",
        "read_all": "read_all_permission",
        "create": "create_permission",
        "update": "update_permission",
        "update_all": "update_all_permission",
        "delete": "delete_permission",
        "delete_all": "delete_all_permission",
    }
    field_name = field_map.get(action)
    if field_name is None:
        return False

    value = getattr(rule, field_name, False)
    if action in ("read_all", "create", "update_all", "delete_all"):
        return bool(value)

        # Действия, зависящие от владельца (read/update/delete "свои"):
    if action in ("read", "update", "delete"):
        if not is_owner:
            print("ACL DEBUG: not owner for owner-only action -> False")
            return False
        return bool(value)

    return bool(value)
