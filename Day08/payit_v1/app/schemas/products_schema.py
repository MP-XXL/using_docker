from pydantic import BaseModel, Field, validator
from datetime import datetime
from ..enums import ProductCategory

class Product(BaseModel):
    user_id: int
    name: str = Field(min_length=2)
    price: float
    quantity: int
    category: ProductCategory

class ProductResponse(Product):
    created_at: datetime
    updated_at: datetime