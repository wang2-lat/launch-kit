from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Product(BaseModel):
    name: str
    description: str
    target_audience: str
    stage: str


class ChannelRecommendation(BaseModel):
    channel: str
    score: int
    reason: str


class Campaign(BaseModel):
    id: Optional[int] = None
    product_name: str
    channel: str
    title: str
    url: str
    posted_at: datetime
    clicks: Optional[int] = None
    conversions: Optional[int] = None
