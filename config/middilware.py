from urllib.parse import parse_qs

from accounts.jwt_utils import verify_token, SECRET_KEY


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        qs = scope["query_string"].decode()
        params = parse_qs(qs)
        token = params.get("token", [None])[0]
        print(token)
        payload = verify_token(token, secret=SECRET_KEY)

        print(payload)
        if isinstance(payload, dict):
            scope["user"] = payload.get('user_id')
        else:
            scope["user"] = None

        return await self.inner(scope, receive, send)
