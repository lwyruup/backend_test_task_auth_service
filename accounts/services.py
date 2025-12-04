from typing import Optional
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from django.utils import timezone as dj_tzone
from .models import AuthSession, User

def create_auth_session(user:User, hours: int = 24) -> AuthSession:
    token = token_urlsafe(32)
    now = dj_tzone.now()
    expires_at = now + timedelta(hours=hours)

    session = AuthSession.objects.create(key=token, user=user, expire_date=expires_at, is_active=True,)
    return session

def get_user_by_token(token: str) -> Optional[User]:
    if not token:
        return None
    now = dj_tzone.now()

    try:
        session = AuthSession.objects.select_related("user").get(key=token,is_active=True,)
    except AuthSession.DoesNotExist:
        return None

    if session.expire_date < now:
        session.is_active = False
        session.save(update_fields=["is_active"])
        return None

    if not session.user.is_active:
        return None

    return session.user

def deactivate_session_by_token(token: str) -> bool:
    if not token:
        return False
    try:
        session = AuthSession.objects.get(key=token, is_active=True)
    except AuthSession.DoesNotExist:
        return False

    session.is_active = False
    session.save(update_fields=["is_active"])
    return True

def deactivate_all_sessions(user: User) -> int:
    return AuthSession.objects.filter(user=user, is_active=True).update(is_active=False)