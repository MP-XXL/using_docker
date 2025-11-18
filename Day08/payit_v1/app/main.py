from fastapi import FastAPI, status, HTTPException
from .models.base import Base
from .database import get_db, engine
from .models.users_model import User
from .models.products_model import Product
from sqlalchemy.exc import OperationalError
from .routes import users_routes, products_routes
import time

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def db_and_table_init():
    retries = 10
    for i in range(retries):
        try:
            logger.info("STARTING APPLICATION!")
            Base.metadata.create_all(bind=engine)
            logger.info("DATABASE INITIALIZED SUCCESSFULLY!")
            break
        except OperationalError as e:
            logger.warning(f"MySQL NOT READY, RETRYING ({i+1}/{retries}) {e}...")
            time.sleep(3)
        except Exception as e:
            logger.info(f"DATABASE INITIALIZATION FAILED: {e}")

app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "market place..."
    )

app.include_router(users_routes.router)
app.include_router(products_routes.router)
@app.on_event("startup")
def on_startup():
    db_and_table_init()

