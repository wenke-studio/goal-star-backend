from ninja import NinjaAPI

api = NinjaAPI()
api.add_router("user", "user.views.router")
api.add_router("goal", "goal.views.router")
