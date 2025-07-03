from ninja.errors import AuthenticationError, AuthorizationError
from ninja.security import HttpBearer

from .clerk import is_signed_in
from .models import User


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            if clerk_id := is_signed_in(request):
                user = User.objects.get(username=clerk_id)
                request.user = user
                return user  # request.auth by ninja
            raise AuthenticationError()

        except User.DoesNotExist:
            raise AuthorizationError()
        except Exception:
            raise AuthenticationError()
