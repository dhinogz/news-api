from django.http import HttpRequest, HttpResponse
from ninja import Router, Form, Schema

# from ninja.security import django_auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


router = Router(tags=["auth"])


@router.post("/login/", response={200: str, 401: str})
def handle_login(request, username: Form[str], password: Form[str]):
    user = authenticate(username=username, password=password)
    if not user:
        return 401, "wrong auth"

    login(request, user)

    return 200, "successful login"


@router.post("/logout/")
def handle_logout(request):
    logout(request)

    return "Logout successful"


class UserResponse(Schema):
    username: str
    first_name: str
    last_name: str


@router.get("/user/", response={200: UserResponse})
def get_current_user(request: HttpRequest):
    if not request.user.is_authenticated:
        return 401, "Not authenticated"

    return request.user


class UserIn(Schema):
    username: str
    password: str
    first_name: str
    last_name: str


@router.post("/user/")
def create_user(request: HttpRequest, response: HttpResponse, payload: UserIn):
    response["content-type"] = "text/plain"
    if not request.user.is_superuser:
        return "Not authorized, my dude"
    try:
        user = User.objects.create_user(
            username=payload.username,
            password=payload.password,
        )
        user.first_name = payload.first_name
        user.last_name = payload.last_name
        user.save()
    except ValueError:
        return 500, "Could not create user"

    return "User created"
