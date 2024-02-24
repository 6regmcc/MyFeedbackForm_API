from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Sequence
from datetime import datetime

from core.database import Base


class SurveyPageDB(Base):
    __tablename__ = "pages"
    page_id = Column(Integer, primary_key=True, index=True)
    page_title =  Column(String(300))
    page_description = Column(String(500))
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)

    survey_id = Column(Integer, ForeignKey('surveys.survey_id'), nullable=False)