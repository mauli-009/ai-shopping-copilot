from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductIn, ProductOut
from app.crud.product import upsert_product
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/analyze", response_model=ProductOut)
def analyze_product(
    data: ProductIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # route is protected
):
    # Phase 1: just store it. Phase 2 will add Redis cache + Groq AI here.
    product = upsert_product(db, data)
    return product