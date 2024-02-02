from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from datetime import datetime

from core.database import Base


class UserModel(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    registered_on = Column(DateTime, nullable=True, default=None)
    updated_on = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_on = Column(DateTime, nullable=False, server_default=func.now())



