from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Sequence
from datetime import datetime

from core.database import Base



class Question(Base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True, index=True)
    question_type = Column(String(50), nullable=False)
    question_variant = Column(String(50), nullable=False)
    question_text = Column(String(300), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    page_id = Column(Integer, ForeignKey('pages.page_id'), nullable=False)
    survey_id = Column(Integer, ForeignKey('surveys.survey_id'), nullable=False)



class CloseEndedAnswerChoice(Base):
    __tablename__ = "close_ended_answer_choices"
    choice_id = Column(Integer, primary_key=True, index=True)
    choice_label = Column(String(300), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
