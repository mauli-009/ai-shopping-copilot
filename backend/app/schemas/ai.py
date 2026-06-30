from pydantic import BaseModel
from typing import List


class ProductAnalysisRequest(BaseModel):
    external_id: str
    title: str
    brand: str | None = None
    price: float | None = None
    description: str | None = None


class ProductAnalysis(BaseModel):
    worth_buying: bool
    score: float
    fabric: str
    value_for_money: str
    suitable_for: List[str]
    recommendation: str

class ReviewSummaryRequest(BaseModel):
    external_id: str
    title: str
    reviews: List[str]


class StyleScoreRequest(BaseModel):
    external_id: str
    title: str
    brand: str | None = None
    price: float | None = None
    description: str | None = None


class ChatRequest(BaseModel):
    title: str
    brand: str | None = None
    price: float | None = None
    description: str | None = None
    question: str