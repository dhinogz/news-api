from datetime import datetime

from django.http import HttpRequest, HttpResponse
from ninja import Router
from .schemas import StoryIn, StoryResponse, ListStoryResponse
from .models import Story
from .helpers import validate_story
# from django.contrib.auth.models import User

router = Router(tags=["stories"])


@router.get("", response={200: ListStoryResponse, 404: str, 503: str})
def fetch_stories(
    request: HttpRequest,
    response: HttpResponse,
    story_cat="*",
    story_region="*",
    story_date="*",
):
    query = Story.objects

    if story_cat != "*":
        query = query.filter(category=story_cat)
    if story_region != "*":
        query = query.filter(region=story_region)
    if story_date != "*":
        try:
            story_date = datetime.strptime(story_date, "%d/%m/%Y")
        except ValueError:
            return 503, "date query param format is incorrect"
        query = query.filter(date__gte=story_date)

    stories = query.all()

    if not stories:
        response["content-type"] = "text/plain"
        return 404, "No stories found"

    stories_response = []
    for s in stories:
        stories_response.append(
            StoryResponse(
                key=str(s.key),
                headline=s.headline,
                story_details=s.details,
                story_cat=s.category,
                story_region=s.region,
                story_date=s.date.strftime("%d/%m/%Y"),
                author=f"{s.author.first_name} {s.author.last_name}",
            )
        )
    return 200, ListStoryResponse(stories=stories_response)


@router.post("", response={201: str, 503: str})
def create_story(
    request: HttpRequest,
    response: HttpResponse,
    payload: StoryIn
):
    response["content-type"] = "text/plain"

    if not request.user.is_authenticated:
        return 503, "Not authenticated"

    validate_story(payload)

    try:
        Story.objects.create(**payload.dict(), author=request.user)
    except ValueError:
        return 503, "Could not create story. Try again."

    return 201, "Story created"


@router.delete("/{story_id}", response={200: None, 503: str})
def delete_story(request: HttpRequest, response: HttpResponse, story_id: int):
    if not request.user.is_authenticated:
        response["content-type"] = "text/plain"
        return 503, "Not authenticated"

    try:
        story = Story.objects.get(key=story_id)
    except Story.DoesNotExist:
        response["content-type"] = "text/plain"
        return 503, "Story with that ID does not exist."

    story.delete()


@router.get("/{story_id}", response={200: StoryResponse, 404: str})
def fetch_story(request: HttpRequest, response: HttpResponse, story_id: int):
    try:
        s = Story.objects.get(key=story_id)
    except Story.DoesNotExist:
        response["content-type"] = "text/plain"
        return 404, "Story with that ID does not exist."

    story = StoryResponse(
        key=str(s.key),
        headline=s.headline,
        story_details=s.details,
        story_cat=s.category,
        story_region=s.region,
        story_date=s.date.strftime("%d/%m/%Y"),
        author=f"{s.author.first_name} {s.author.last_name}",
    )

    return story
