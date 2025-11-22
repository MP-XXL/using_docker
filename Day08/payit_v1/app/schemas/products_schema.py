from pydantic import BaseModel, Field, validator
from datetime import datetime
from ..enums import Category

class Product(BaseModel):
    user_id: int
    name: str = Field(min_length=2)
    price: float
    quantity: int
    category: Category

class ProductResponse(Product):
    created_at: datetime
    updated_at: datetime