from pydantic import BaseModel


class ProductCategory(BaseModel):
    category_name: str