from .schemas import StoryIn
from ninja.errors import ValidationError


MAX_HEADLINE_LEN = 64
MAX_DETAILS_LEN = 128


def validate_story(story_in: StoryIn) -> None:
    if len(story_in.headline) > MAX_HEADLINE_LEN:
        raise ValidationError(
            errors=[
                {"msg": "Story headline cannot be longer than 64 characters"}
            ]
        )
    if len(story_in.details) > MAX_DETAILS_LEN:
        raise ValidationError(
            errors=[
                {"msg": "Story details cannot be longer than 128 characters"}
            ]
        )
