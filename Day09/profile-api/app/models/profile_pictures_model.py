from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func, Enum
from sqlalchemy.orm import relationship
from .base import Base

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, nullable=False,index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    image_url = Column(String(200), nullable=True)
    public_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)