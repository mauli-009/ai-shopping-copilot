from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.ai import (
    ai_test,
    analyze_product,
    summarize_reviews,
    style_score,
    shopping_chat,
)
from app.core.security import get_current_user
from app.core.cache import cache_get, cache_set
from app.models.user import User
from app.schemas.ai import (
    ProductAnalysisRequest,
    ReviewSummaryRequest,
    StyleScoreRequest,
    ChatRequest,
)

router = APIRouter(prefix="/ai", tags=["ai"])


class TestRequest(BaseModel):
    prompt: str


@router.post("/test")
def test_ai(body: TestRequest, current_user: User = Depends(get_current_user)):
    reply = ai_test(body.prompt)
    return {"reply": reply}


@router.post("/product-analysis")
def product_analysis(
    body: ProductAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    cache_key = f"analysis:{body.external_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    result = analyze_product(body.model_dump())
    cache_set(cache_key, result, ttl_seconds=43200)
    return result


@router.post("/review-summary")
def review_summary(
    body: ReviewSummaryRequest,
    current_user: User = Depends(get_current_user),
):
    cache_key = f"reviews:{body.external_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    result = summarize_reviews(body.title, body.reviews)
    cache_set(cache_key, result, ttl_seconds=43200)
    return result


@router.post("/style-score")
def style_score_endpoint(
    body: StyleScoreRequest,
    current_user: User = Depends(get_current_user),
):
    cache_key = f"style:{body.external_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    result = style_score(body.model_dump())
    cache_set(cache_key, result, ttl_seconds=43200)
    return result


@router.post("/chat")
def chat_endpoint(
    body: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    # Not cached — every question is different
    reply = shopping_chat(body.model_dump(), body.question)
    return {"reply": reply}