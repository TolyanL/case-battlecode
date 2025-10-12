from dataclasses import dataclass
from .review_settings import REVIEW_COUNT


@dataclass
class PageData:
    title: str
    description: str
    curr_page: str
    max_reviews: int = REVIEW_COUNT
