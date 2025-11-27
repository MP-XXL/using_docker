from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from ..models import products_model, users_model, farmers_model, buyers_model, products_category_model
from ..schemas.products_schema import Product, ProductResponse
from ..middlewares.auth import AuthMiddleware
from datetime import datetime
from typing import List
import os
import aiofiles
from ..enums import Category
from uuid import uuid4
import pymysql

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



router = APIRouter(tags=["Products"])


UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class FileTooLargeError(Exception):
    pass



@router.post("/products")
async def create_product(
    name: str = Form(...),
    image: UploadFile = File(...),
    description: str = Form(...),
    category: Category = Form(...),
    unit_price: int = Form(...),
    quantity: int = Form(...),
    current_user=Depends(AuthMiddleware),
    db: Session = Depends(get_db)):


    
    # user = db.query(users_model.User).filter(users_model.User.id == current_user.id).first()
    # if not new_product:
    #     raise HTTPException(
    #         status_code = status.HTTP_404_NOT_FOUND,
    #         detail = "User ID does not exists!"
    #     )

   
    allowed_extns = ["png", "jpeg", "jpg"]

    file_extn = image.filename.split(".")[-1].lower()
    if not file_extn in allowed_extns:
        raiseError("Invalid file extension", status.HTTP_400_BAD_REQUEST)

    try:
        file_name = f"{uuid4()}.{file_extn}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        async with aiofiles.open(file_path, "wb") as output_file:
            content = await image.read()
            file_size = len(content)
            if file_size > 5000000:
                raise FileTooLargeError()
            await output_file.write(content)
    
    except FileTooLargeError:
        return {
            "message": "File size must not be greater than 5MB"
        }
        
    except Exception as e:
        raiseError("Internal Server Erro", status.HTTP_500_INTERNAL_SERVER_ERROR)

 
    db_farmer = db.query(farmers_model.Farmer).filter(farmers_model.Farmer.user_id == current_user.id).first()
    if not db_farmer:
        db_farmer = farmers_model.Farmer(user_id=current_user.id)
        db.add(db_farmer)
        db.commit()
        db.refresh(db_farmer)
    
    db_category = db.query(products_category_model.ProductCategory).filter(products_category_model.ProductCategory.category_name == category.value).first()
    if not db_category:
        db_category = products_category_model.ProductCategory(category_name=category.value)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
   

    try:
        image_url = f"static/uploads/{file_name}"
        
        new_product = products_model.Product(
            name = name,
            description = description,
            image_url= image_url,
            farmer_id = db_farmer.id,
            category_id = db_category.id,
            unit_price = unit_price,
            quantity= quantity
            )
        

        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {
            "success": True,
            "detail": new_product,
            "message": "Product created successfully"
            }
    except pymysql.DataError as e:
        raiseError(e, status.HTTP_500_INTERNAL_SERVER_ERROR)

def raiseError(e, status_code):
    logger.error(f"failed to created record error: {e}")
    raise HTTPException(
        status_code = status_code,
        detail = {
            "status": "error",
            "message": f"{e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )


@router.get("/products/{product_id}")
def get_a_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(products_model.Product).filter(products_model.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product with ID not found"
        )

    return product


@router.get("/farmers/products/{farmer_id}")
def get_all_products_from_a_farmer(farmer_id: int, db: Session = Depends(get_db)):
    return db.query(products_model.Product).filter(products_model.Product.farmer_id == farmer_id).all()
    if not True:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Farmer with ID not found"
        )


@router.put("/products/{product_id}") # REMEMBER TO CHECK IF A USER CAN UPDATE ANOTHER USER'S PRODUCT
def update_product(product_id: int, product: Product, current_user=Depends(AuthMiddleware), db: Session = Depends(get_db)):
    user = db.query(products_model.Product).filter(products_model.Product.farmer_id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Farmer with ID not found"
        )
    updated_product = db.query(products_model.Product).filter(products_model.Product.id == product_id).first()
    if not update_product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Product with ID not found"
        )
    
    for field, value in product.dict().items():
        setattr(updated_product, field, value)

    db_category = db.query(products_category_model.ProductCategory).filter(products_category_model.ProductCategory.category_name == updated_product.category.value).first()
    if not db_category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Category to update not found"
        )
    # updated_product.category_id = db_category.id   "OR"
    setattr(updated_product, "category_id", db_category.id)

    db.commit()
    db.refresh(updated_product)
    return updated_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, current_user=Depends(AuthMiddleware), db: Session = Depends(get_db)):
    user = db.query(products_model.Product).filter(products_model.Product.farmer_id == current_user.id)
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

@router.get("/products")
def get_all_products(db: Session=Depends(get_db)):
    return db.query(products_model.Product).all()
