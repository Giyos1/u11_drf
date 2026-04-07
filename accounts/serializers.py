from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('failed')
        return {"user": user}


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'last_name': {'required': False},
        }

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        password = data.get('password')
        if password != confirm_password:
            raise serializers.ValidationError('password and confirm_password are not equal')
        return data

    def create(self, data):
        return User.objects.create_user(**data)
