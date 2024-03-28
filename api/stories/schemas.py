from ninja import Schema
import enum
from typing import Optional


class CategoryEnum(str, enum.Enum):
    pol = "pol"
    art = "art"
    tech = "tech"
    trivia = "trivia"


class RegionEnum(str, enum.Enum):
    uk = "uk"
    eu = "eu"
    w = "w"


class StoryResponse(Schema):
    key: str
    headline: str
    story_details: str
    story_cat: str
    story_region: str
    story_date: str
    author: Optional[str] = None


class ListStoryResponse(Schema):
    stories: list[StoryResponse]


class StoryIn(Schema):
    headline: str
    details: str
    category: CategoryEnum
    region: RegionEnum

    class Config:
        json_schema_extra = {
            "example": {
                "headline": "Example headline!",
                "details": "This is an example details",
                "category": "tech",
                "region": "uk",
            },
        }
