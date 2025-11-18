from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from database.database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))



