from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from core.database import Base


class SurveyModel(Base):
    __tablename__ = "surveys"
    survey_id = Column(Integer, primary_key=True, index=True)
    survey_name = Column(String(300))
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    #owner = relationship("Owner", back_populates = "surveys")
