from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func, Enum, DECIMAL
from .base import Base
from ..enums import TransactionType

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    txn_id = Column(Integer, nullable=False)
    payment_gateway = Column(String(30))
    payment_type = Column(ENUM(TransactionType), nullable=False)
    payload(JSON) = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
  