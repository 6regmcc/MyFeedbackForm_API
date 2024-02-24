from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Sequence, Enum
from datetime import datetime

from core.database import Base
from surveys.pages.questions.questions_schemas import OpenEndedAnswerChoiceRequest


class QuestionDB(Base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True, index=True)
    question_type = Column(String(50), nullable=False)
    question_variant = Column(String(50), nullable=False)
    question_text = Column(String(300), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    page_id = Column(Integer, ForeignKey('pages.page_id'), nullable=False)
    question_position = Column(Integer, nullable=False, unique=True)
    survey_id = Column(Integer, ForeignKey('surveys.survey_id'), nullable=False)


class CloseEndedAnswerChoice(Base):
    __tablename__ = "close_ended_answer_choices"
    choice_id = Column(Integer, primary_key=True, index=True)
    choice_label = Column(String(300), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)


class OpenEndedAnswerChoice(Base):
    __tablename__ = "open_ended_answer_choices"
    choice_id = Column(Integer, primary_key=True, index=True)
    open_ended_choice_type = Column(String(50), nullable=False)
    choice_label = Column(String(300))
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)


