from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.jwt_utils import verify_token, SECRET_KEY
from accounts.models import User


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header: return None
        try:
            type_, token = header.split()  # Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc2MzUwNzIzLCJpYXQiOjE3NzYzNTA0MjMsImp0aSI6IjY0MzAzNjQzMzBlZTQ2MzI4ZDY0ZGVlZTUxOWZiZDFjIiwidXNlcl9pZCI6IjEifQ.iBhD97A0ldIGb0bQNbHDDBEBU650lJ8zbLIjTjJ5ETs
        except ValueError:
            raise AuthenticationFailed('Noto\'g\'ri format')
        if type_.lower() != 'bearer':
            raise AuthenticationFailed('Bearer kerak')
        payload = verify_token(token, SECRET_KEY, 'access')
        if not isinstance(payload, dict):
            raise AuthenticationFailed(payload)
        user = User.objects.get(id=payload['user_id'])
        return user, None
