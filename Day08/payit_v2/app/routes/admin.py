# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from ..database import get_db
# from ..models.products_category import ProductCategory
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# router = APIRouter()

# @router.post("/")
# def init_products_category(db: Session= Depends(get_db)):
#     category_names=["grains","tubers","cereals","fruits","livestock","vegetables","oils","latex"]
    
#     try:
#         count = db.query(ProductCategory).count()
#         if count == 0:
#             for cat_name in category_names:
#                 new_category = ProductCategory(category_name=cat_name)
#                 db.add(new_category)
#         db.commit()
#         db.refresh(new_category)
#         logger.info(f"PRODUCT CATEGORY POPULATED SUCCESSFULLY")
#     except Exception as e:
#         logger.info(f"PRODUCT CATEGORY DATABASE FAILED : {e}")