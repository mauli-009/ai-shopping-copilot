from pydantic import BaseModel
from typing import Optional


class ProductIn(BaseModel):
    external_id: str
    title: str
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    description: Optional[str] = None
    source_url: Optional[str] = None


class ProductOut(ProductIn):
    id: int
    model_config = {"from_attributes": True}