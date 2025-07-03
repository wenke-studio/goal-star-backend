from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone
from ninja import Router

from .models import Goal

router = Router(tags=["tasks"])


# TODO: those tasks shoulde be celery schedule tasks


@router.post("/task/check-overdue-goals")
def check_overdue_goals(request):
    """Check for goals past deadline and mark as overdue"""
    today = timezone.now().date()

    # Find active goals past deadline
    overdue_goals = Goal.objects.filter(status=Goal.Status.ACTIVE, deadline__lt=today)

    for goal in overdue_goals:
        goal.mark_overdue()
        # send_mail(
        #     "Goal Overdue",
        #     "Your goal has been marked as overdue",
        #     "noreply@wenke-studio.com",
        #     [goal.user.email],
        # )
        # send_mail(
        #     "Goal Overdue",
        #     "Your goal has been marked as overdue",
        #     "noreply@wenke-studio.com",
        #     [goal.friendEmail],
        # )

    return f"Marked {overdue_goals.count()} goals as overdue"


@router.post("/task/check-expired-verifications")
def check_expired_verifications(request):
    """Mark goals as overdue if friend hasn't verified within 3 days"""
    three_days_ago = timezone.now() - timedelta(days=3)

    # Find goals with verification sent over 3 days ago
    expired_goals = Goal.objects.filter(
        status=Goal.Status.OVERDUE, deadline__lt=three_days_ago
    )

    for goal in expired_goals:
        send_mail(
            "Goal Expired",
            "Your goal has expired",
            "noreply@wenke-studio.com",
            [goal.user.email],
        )

    return (
        f"Marked {expired_goals.count()} goals as overdue due to expired verification"
    )
