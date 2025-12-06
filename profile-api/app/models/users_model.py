from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func, Enum
from sqlalchemy.orm import relationship
from .base import Base
# from ..enums import Gender

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False,index=True)
    name = Column(String(50), min_length=20, max_length=50, nullable=False)
    email= Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship('Image', cascade='all, delete', backref='users')