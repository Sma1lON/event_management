from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Отримати JWT токен для автентифікації",
        responses={
            200: "{'access': 'token', 'refresh': 'token'}",
            401: "Неправильні облікові дані"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
