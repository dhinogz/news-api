from django.http import HttpResponse
from stories.views import router as stories_router
from .auth import router as auth_router
from ninja import NinjaAPI
from ninja.errors import ValidationError

api = NinjaAPI(title="News API")


api.add_router("", auth_router)
api.add_router("/stories", stories_router)


@api.exception_handler(ValidationError)
def validation_error(request, exc):
    msg = exc.errors[0]["msg"]
    response = HttpResponse(msg, status=422)
    response["content-type"] = "text/plain"
    response.status_code = 503

    return response
