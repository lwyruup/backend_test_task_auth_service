from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
# from .models import User
from .serializers import (RegisterSerializer, LoginSerializer, UserSerializer, AdminUserSerializer, SelfUserUpdateSerializer)
from .services import create_auth_session, deactivate_session_by_token, deactivate_all_sessions
from access_control.permissions import HasAccess
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from .models import User
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse

## extend.schema используем для корректного отображения полей в Swagger

@extend_schema(tags=["auth"], summary="Регистрация пользователя", description="Регистрация нового пользователя по email и паролю.", request=RegisterSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(description="Ошибка валидации входных данных"),})
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)



LoginResponseSerializer = inline_serializer(
    name="LoginResponse",
    fields={
        "token": serializers.CharField(),
        "user": UserSerializer(),
    },
)

@extend_schema(
    tags=["auth"],
    summary="Логин пользователя",
    description="Логин по email и паролю. В ответе возвращается токен сессии и данные пользователя.",
    request=LoginSerializer,
    responses={
        200: LoginResponseSerializer,
        401: OpenApiResponse(description="Неверные учетные данные"),
    },
)
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={"request": request},)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        session = create_auth_session(user)

        return Response(
            {
                "token": session.key,
                "user": UserSerializer(user).data,
            }, status=status.HTTP_200_OK)


from .services import get_user_by_token

@extend_schema(request=SelfUserUpdateSerializer, responses={200: UserSerializer})
class MeView(APIView):
    def _get_current_user(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        token = None

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()


        if not token:
            return None

        return get_user_by_token(token)

    @extend_schema(
        tags=["auth"],
        summary="Текущий пользователь",
        description="Возвращает данные текущего залогиненного пользователя.",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Неавторизован"),
        },
    )
    def get(self, request):
        user = self._get_current_user(request)
        if user is None:
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request):
        return self._update(request)

    def patch(self, request):
        return self._update(request)

    def _update(self, request):
        user = self._get_current_user(request)

        serializer = SelfUserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = self._get_current_user(request)
        if user is None:
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        #мягкое удаление пользователя
        user.is_active = False
        user.save(update_fields=["is_active"])
        deactivate_all_sessions(user)

        return Response({"detail": "Аккаунт деактивирован"}, status=status.HTTP_200_OK)



class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [HasAccess]
    business_element_code = "users"
    permission_action = "read_all"

class AdminUserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

    permission_classes = [HasAccess]
    business_element_code = "users"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_action = "read_all"
        elif self.request.method == "POST":
            self.permission_action = "create"
        return super().get_permissions()

class AdminUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

    permission_classes = [HasAccess]
    business_element_code = "users"

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_action = "read_all"      # или "read"
        elif self.request.method in ("PUT", "PATCH"):
            self.permission_action = "update_all"
        elif self.request.method == "DELETE":
            self.permission_action = "delete_all"
        return super().get_permissions()

    def perform_destroy(self, instance: User) -> None:
        instance.is_active = False
        instance.save(update_fields=["is_active"])

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        token = None

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return Response(
                {"detail": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        success = deactivate_session_by_token(token)
        if not success:
            return Response(
                {"detail": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response({"detail": "Loged out"}, status=status.HTTP_200_OK)
