from enum import Enum
from typing import Optional

from pydantic import BaseModel
from datetime import datetime

from core.pydantic_basemodel_config import NoExtraBaseModel


class OpenEndedAnswerChoiceEnum(str, Enum):
    answer_choice = "answer_choice"
    other_answer_choice = "other_answer_choice"


class OpenEndedAnswerChoiceRequest(NoExtraBaseModel):
    open_ended_choice_type: str
    choice_label: str | None


class OpenEndedAnswerChoiceData(OpenEndedAnswerChoiceRequest):
    question_id: int


class OpenEndedAnswerChoiceResponse(OpenEndedAnswerChoiceData):
    choice_id: int
    date_created: datetime
    date_modified: datetime


class QuestionTypeEnum(str, Enum):
    closed_ended = "closed_ended"
    open_ended = "open_ended"


class QuestionVariantEnum(str, Enum):
    single_choice = "single_choice"
    multi_choice = "multi_choice"


class ClosedAnswerChoiceRequest(NoExtraBaseModel):
    choice_label: str


class CreateQuestionRequest(NoExtraBaseModel):
    question_type: QuestionTypeEnum
    question_variant: QuestionVariantEnum
    question_text: str
    answer_choices: list[OpenEndedAnswerChoiceRequest | ClosedAnswerChoiceRequest] | None = None
    has_other_answer_choice: bool = False

    class Config:
        orm_mode = True


class CreateQuestionData(CreateQuestionRequest):
    survey_id: int
    page_id: int
    question_position: int


class CreateQuestionResponse(CreateQuestionData):
    question_id: int
    date_created: datetime
    date_modified: datetime
    answer_choices: list[OpenEndedAnswerChoiceRequest | ClosedAnswerChoiceRequest] | None


class ClosedAnswerChoiceRequestData(ClosedAnswerChoiceRequest):
    question_id: int


class CreateMultipleChoiceQuestionRequest(CreateQuestionRequest):
    answer_choices: list[ClosedAnswerChoiceRequest]


class ClosedAnswerChoice(ClosedAnswerChoiceRequest):
    choice_id: int
    date_created: datetime
    date_modified: datetime

    class Config:
        orm_mode = True


class CreateMultipleChoiceQuestionData(NoExtraBaseModel):
    question_type: str = "closed_ended"
    question_variant: str = "single_choice"
    question_text: str
    survey_id: int
    page_id: int
    answer_choices: list[ClosedAnswerChoiceRequest]


class MultipleChoiceQuestion(CreateQuestionResponse):
    answer_choices: list[ClosedAnswerChoice]

    class Config:
        orm_mode = True


class CreateOpenEndedQuestionData(CreateQuestionData):
    answer_choices: list[OpenEndedAnswerChoiceRequest]

    class Config:
        orm_mode = True


class OpenEndedQuestion(CreateQuestionResponse):
    answer_choices: list[OpenEndedAnswerChoiceResponse]

    class Config:
        orm_mode = True


class TestCreateClosedChoice(NoExtraBaseModel):
    choice_label: str

    class Config:
        extra = "forbid"
