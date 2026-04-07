from django.contrib.auth import login, logout
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.serializers import LoginSerializer, UserSerializer, RegistrationSerializer


class AuthViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'register':
            return RegistrationSerializer
        else:
            return LoginSerializer

    def get_permissions(self):
        if self.action in ('logout_user', 'sessions'):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        serializers = LoginSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.validated_data.get('user')
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False)
    def logout_user(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def sessions(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, serializer_class=RegistrationSerializer)
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
