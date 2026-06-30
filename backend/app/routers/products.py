from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductIn, ProductOut
from app.crud.product import upsert_product
from app.core.security import get_current_user
from app.core.cache import cache_get, cache_set
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/analyze", response_model=ProductOut)
def analyze_product(
    data: ProductIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cache_key = f"product:{data.external_id}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    product = upsert_product(db, data)
    result = ProductOut.model_validate(product).model_dump()
    cache_set(cache_key, result, ttl_seconds=43200)
    return result