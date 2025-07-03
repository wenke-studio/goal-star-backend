from ninja import ModelSchema

from .models import Goal


class GoalListSchema(ModelSchema):
    class Meta:
        model = Goal
        exclude = ["verification_token", "user"]


class GoalCreateSchema(ModelSchema):
    class Meta:
        model = Goal
        fields = ["title", "description", "deadline", "friendEmail"]


class GoalRetrieveSchema(ModelSchema):
    class Meta:
        model = Goal
        fields = [
            "title",
            "description",
            "deadline",
            "friendEmail",
            "status",
        ]
