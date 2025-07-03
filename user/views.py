import logging
from typing import Literal

from ninja import Router, Schema
from ninja.errors import AuthenticationError

from .clerk import get_clerk_user, is_signed_in, update_clerk_user
from .models import User

logger = logging.getLogger(__name__)

router = Router(tags=["user"])


class OnboardingSchema(Schema):
    appName: Literal["goalStar"]


@router.post("/onboarding")
def onboarding(request, data: OnboardingSchema):
    if clerk_id := is_signed_in(request):
        _, created = User.objects.get_or_create(username=clerk_id)
        if not created:
            logger.warning("user already exists, %s", clerk_id)

        if clerk_user := get_clerk_user(user_id=clerk_id):
            app_metadata = clerk_user.private_metadata.get(data.appName, {})
            app_metadata["onboarding"] = "complete"
            update_clerk_user(
                user_id=clerk_id,
                private_metadata={
                    data.appName: app_metadata,
                    **clerk_user.private_metadata,
                },
            )
            return {"detail": "created"}
        else:
            logger.error("[clerk] signed-in user not found, %s", clerk_id)
            return 502, {"detail": "clerk user not found"}
    logger.error("onboarding, %s", request.headers.get("Authorization"))
    raise AuthenticationError()
