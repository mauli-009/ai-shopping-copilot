from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductIn


def upsert_product(db: Session, data: ProductIn) -> Product:
    existing = (
        db.query(Product).filter(Product.external_id == data.external_id).first()
    )
    if existing:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing

    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product