from ninja import Router
from ninja.errors import HttpError

from user.authentication import AuthBearer
from utils.schemas import DetailSchema, ListSchema, ObjectSchema

from .models import Goal
from .schemas import (
    GoalCreateSchema,
    GoalListSchema,
    GoalRetrieveSchema,
)

router = Router(tags=["goal"], auth=AuthBearer())


@router.get("", response={200: ListSchema[GoalListSchema]})
def list_goals(request):
    goals = Goal.objects.filter(user=request.user)
    return {"items": goals}


@router.post("", response={201: DetailSchema, 409: DetailSchema})
def create_goal(request, goal: GoalCreateSchema):
    if Goal.objects.has_active_goal(request.user):
        raise HttpError(409, "You already have an active goal")

    goal = Goal.objects.create(
        **goal.dict(),
        status=Goal.Status.ACTIVE,
        user=request.user,
    )
    return 201, {"detail": "created"}


@router.get(
    "/current", response={200: ObjectSchema[GoalRetrieveSchema], 404: DetailSchema}
)
def retrieve_current_goal(request):
    try:
        goal = Goal.objects.get(
            user=request.user, status__in=[Goal.Status.ACTIVE, Goal.Status.OVERDUE]
        )
        return 200, {"item": goal}
    except Goal.DoesNotExist:
        raise HttpError(404, "No active goal found")


@router.delete("/current", response={200: DetailSchema, 404: DetailSchema})
def disable_current_goal(request):
    if not Goal.objects.has_active_goal(request.user):
        raise HttpError(404, "No active goal found")

    goal = Goal.objects.get(user=request.user, status=Goal.Status.ACTIVE)
    goal.cancel()
    return 200, {"detail": "Goal disabled"}


@router.get("/complete/{token}", auth=None, response={200: DetailSchema})
def complete_by_frient(request, token: str):
    goal = Goal.objects.get(verification_token=token)
    goal.complete_by_friend()
    return 200, {"detail": "Goal completed"}


@router.patch("/complete", response={200: DetailSchema})
def complete_by_self(request):
    goal = Goal.objects.get(user=request.user, status=Goal.Status.ACTIVE)
    goal.complete_by_self()
    return 200, {"detail": "Goal completed"}
