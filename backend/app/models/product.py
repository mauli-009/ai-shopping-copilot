from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, index=True)   # site's own product id/url hash
    title = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String)
    price = Column(Float)
    image = Column(String)
    description = Column(Text)
    source_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())