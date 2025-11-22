from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends
from ..models import products_model, users_model
from ..schemas.products_schema import Product, ProductResponse
from datetime import datetime
from typing import List



router = APIRouter(tags=["Products"])



@router.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    new_product = db.query(users_model.User).filter(users_model.User.id == product.user_id).first()
    if not new_product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User ID does not exists!"
        )

    new_product = products_model.Product(
        **product.model_dump()
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return(new_product)

@router.get("/products/{product_id}")
def get_a_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(products_model.Product).filter(products_model.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product with ID not found"
        )

    return product

@router.put("/products/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    updated_product = db.query(products_model.Product).filter(products_model.Product.id == product_id).first()
    if not update_product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product with ID not found"
        )

    for field, value in product.dict().items():
        setattr(updated_product, field, value)

    db.commit()
    db.refresh(updated_product)
    return updated_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_to_delete = db.query(products_model.Product).filter(products_model.Product.id == product_id).first()
    if not product_to_delete:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product with ID not found"
        )


    db.delete(product_to_delete)
    db.commit()
    raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Product deleted successfully"
    )

@router.get("/products", response_model=List[ProductResponse])
def get_all_products(db: Session=Depends(get_db)):
    return db.query(products_model.Product).all()
