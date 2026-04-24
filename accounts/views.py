from django.contrib.auth import login, logout
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.jwt_utils import create_tokens, blacklisted_users, verify_token, REFRESH_SECRET, refresh_access_token
from accounts.serializers import LoginSerializer, UserSerializer, RegistrationSerializer, JWTLoginSerializer, \
    BlackListSerializer


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'register':
            return RegistrationSerializer
        if self.action == 'create':
            return LoginSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ('logout_user', 'sessions'):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            user = serializers.validated_data.get('user')
            token = user.token
            return Response({'token': token}, status=status.HTTP_201_CREATED)
            # login(request, user)
            # return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False)
    def logout_user(self, request):
        # session logout
        # logout(request)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def sessions(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JWTAuthViewSet(viewsets.GenericViewSet):
    serializer_class = JWTLoginSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ('sessions', 'logout_user'):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'logout_user':
            return BlackListSerializer
        elif self.action == 'refresh_token':
            return BlackListSerializer
        else:
            return JWTLoginSerializer

    # -> default method lar -> 1. list()  ->
    # # GET
    # def list(self, request):
    #     pass
    #
    # # post/1/ GET
    # def retrieve(self, request, pk):
    #     pass
    #
    # # post/  POST
    # def create(self, request):
    #     pass
    #
    # # post/1/ PATCH
    # def partial_update(self, request, pk):
    #     pass
    #
    # # post/1 PUT
    # def update(self, request, pk):
    #     pass
    #
    # # post/1/  # DELETE
    # def destroy(self, request, pk):
    #     pass

    @action(methods=['post'], detail=False)
    def login_user(self, request):
        serializer = JWTLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = create_tokens(user.id)
        return Response(token, status=200)

    @action(methods=['get'], detail=False)
    def sessions(self, request):
        user = request.user  # anonymous user, 1
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def refresh_token(self, request):
        serializer = BlackListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = refresh_access_token(serializer.validated_data['refresh_token'])
        return Response(token, status=200)

    @action(methods=['post'], detail=False)
    def logout_user(self, request):
        serializer = BlackListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blacklisted_users.append(serializer.validated_data['refresh_token'])
        return Response(status=status.HTTP_204_NO_CONTENT)

# login -> API -> request jonatishi kerak front-> username, password-> POST
