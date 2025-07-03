from clerk_backend_api import AuthenticateRequestOptions, Clerk
from clerk_backend_api.models import User as ClerkUser
from clerk_backend_api.security import AuthStatus
from django.conf import settings
from django.http import HttpRequest


def is_signed_in(request: HttpRequest) -> str | None:
    with Clerk(bearer_auth=settings.CLERK_SECRET_KEY) as clerk:
        request_state = clerk.authenticate_request(
            request, AuthenticateRequestOptions()
        )
        if request_state.status == AuthStatus.SIGNED_IN:
            return request_state.payload.get("sub")


def get_clerk_user(user_id: str) -> ClerkUser | None:
    with Clerk(bearer_auth=settings.CLERK_SECRET_KEY) as clerk:
        return clerk.users.get(user_id=user_id)


def update_clerk_user(user_id: str, private_metadata: dict):
    with Clerk(bearer_auth=settings.CLERK_SECRET_KEY) as clerk:
        clerk.users.update(user_id=user_id, private_metadata=private_metadata)
