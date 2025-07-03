import secrets

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import User

nullable = {"default": None, "null": True, "blank": True}


class GoalManager(models.Manager):
    def has_active_goal(self, user: User) -> bool:
        return self.filter(user=user, status=self.model.Status.ACTIVE).exists()


class GoalMixin:
    """
    Active -> Overdue -> Completed/Self-Completed
           -> Cancelled
    """

    def mark_overdue(self):
        if self.status == self.Status.ACTIVE:
            self.status = self.Status.OVERDUE
            self.verification_token = secrets.token_urlsafe(64)
            self.save()

    def complete_by_friend(self):
        if self.status == self.Status.OVERDUE:
            self.status = self.Status.COMPLETED
            self.completed_at = timezone.now()
            self.save()

    def complete_by_self(self):
        if self.status == self.Status.OVERDUE:
            self.status = self.Status.SELF_COMPLETED
            self.completed_at = timezone.now()
            self.save()

    def cancel(self):
        if self.status == self.Status.ACTIVE:
            self.status = self.Status.CANCELLED
            self.completed_at = timezone.now()
            self.save()


class Goal(models.Model, GoalMixin):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        OVERDUE = "overdue", _("Overdue")
        CANCELLED = "cancelled", _("Cancelled")
        COMPLETED = "completed", _("Completed")
        SELF_COMPLETED = "self_completed", _("Self Completed")

    title = models.CharField(max_length=255)
    description = models.TextField(**nullable)
    deadline = models.DateField()
    friendEmail = models.EmailField()
    status = models.CharField(
        max_length=20, default=Status.ACTIVE, choices=Status.choices
    )
    verification_token = models.CharField(max_length=64, unique=True, **nullable)
    completed_at = models.DateTimeField(**nullable)

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    objects = GoalManager()
