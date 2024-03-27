from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Sequence, Enum, UUID, PrimaryKeyConstraint, \
    Boolean
from datetime import datetime

from core.database import Base


class SurveyResponse(Base):
    __tablename__ = 'responses'
    response_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(UUID, index=True, nullable=False, unique=True)
    survey_id = Column(Integer, ForeignKey('surveys.survey_id'), index=True, nullable=False, unique=True)
    collector_id = Column(Integer, ForeignKey('collectors.collector_id'), nullable=False, unique=True, index=True)
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_modified = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)


class ClosedEndedResponses(Base):
    __tablename__ = 'closed_ended_responses'
    response_id = Column(Integer, ForeignKey('responses.response_id'), primary_key=True,  nullable=False, index=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'), primary_key=True, nullable=False, index=True)
    ce_choice_id = Column(Integer, ForeignKey('close_ended_answer_choices.ce_choice_id'), primary_key=True, nullable=False, index=True)
    date_created = Column(DateTime, nullable=False, server_default=func.now())


class OpenEndedResponses(Base):
    __tablename__ = 'open_ended_responses'
    response_id = Column(Integer, ForeignKey('responses.response_id'), primary_key=True, nullable=False, index=True)
    question_id = Column(Integer, ForeignKey('questions.question_id'), primary_key=True, nullable=False, index=True)
    oe_choice_id = Column(Integer, ForeignKey('open_ended_answer_choices.oe_choice_id'), primary_key=True, nullable=False,
                          index=True)
    answer_text = Column(String(500))
    date_created = Column(DateTime, nullable=False, server_default=func.now())


class Collectors(Base):
    __tablename__ = 'collectors'
    collector_id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey('surveys.survey_id'), index=True, nullable=False, unique=True)
    url = Column(String, index=True, nullable=False, unique=True)
    is_open = Column(Boolean, nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=func.now())


