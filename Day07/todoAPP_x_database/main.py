from fastapi import FastAPI, HTTPException
#from database_models.db_model import Base
from database.database import Base, engine
from database_models.db_model import User, Todo
from routes import user_routes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def db_and_table_init():
    retries = 10
    for i in range(retries):
        try:
            logger.info("STARTING APPLICATION!")
            Base.metadata.create_all(bind=engine)
            logger.info("STARTING APPLICATION!")
            break
        except OperationalError as e:
            logger.warning(f"MySQL NOT READY, RETRYING ({i+1}/{retries})...")
            time.sleep(3)
        except Exception as e:
            logger.info(f"DATABASE INITIALIZATION FAILED: {e}")

app = FastAPI()

app.include_router(user_routes.router)
@app.on_event("startup")
def on_startup():
    db_and_table_init()

