from django.contrib.auth.models import AnonymousUser
from .services import get_user_by_token

class AuthTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        token = None

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()

        if token:
            user = get_user_by_token(token)
            if user is not None:
                request.user = user

        return self.get_response(request)


# class AuthTokenMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         user = getattr(request, "user", AnonymousUser())
#         auth_header = request.META.get("HTTP_AUTHORIZATION", "")
#         token = None
#
#         if auth_header.startswith("Bearer "):
#             token = auth_header.split(" ", 1)[1].strip()
#
#         # if token:
#         #     found_user = get_user_by_token(token)
#         #     if found_user is not None:
#         #         user = found_user
#         # request.user = user
#
#         #### тестовый ###
#         if token:
#             user = get_user_by_token(token)
#             if user is not None:
#                 # Только если токен валидный, подменяем request.user
#                 request.user = user
#         ###
#         return self.get_response(request)