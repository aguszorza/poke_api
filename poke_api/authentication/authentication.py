from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from authentication.auth_client import AuthApiClient
from authentication.remote_user import RemoteUser


class RemoteJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise AuthenticationFailed("Authorization header missing")

        user_data = AuthApiClient.get_current_user(auth_header)

        if not user_data:
            raise AuthenticationFailed("Invalid token")

        remote_user = RemoteUser(user_data)
        return (remote_user, None)

    def authenticate_header(self, request):
        return "Bearer"
