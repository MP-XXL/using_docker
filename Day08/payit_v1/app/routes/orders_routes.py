from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.products_category import ProductCategory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["orders"])

@router.post("/orders")
def order_product(db: Session= Depends(get_db)):
    pass
   