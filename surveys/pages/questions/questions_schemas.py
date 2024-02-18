from pydantic import BaseModel
from datetime import datetime


class CreateQuestionRequest(BaseModel):
    question_type: str = "closed_ended"
    question_variant: str = "single_choice"
    question_text: str



class CreateQuestionData(CreateQuestionRequest):
    survey_id: int
    page_id: int

class CreateQuestionResponse(CreateQuestionRequest):
    question_id: int


class ClosedAnswerChoiceRequest(BaseModel):
    choice_label: str

class ClosedAnswerChoiceRequestData(ClosedAnswerChoiceRequest):
    question_id: int


class CreateMultipleChoiceQuestionRequest(CreateQuestionRequest):
    answer_choices: list[ClosedAnswerChoiceRequest]



class ClosedAnswerChoice(ClosedAnswerChoiceRequest):
    choice_id: int
    date_created: datetime
    date_modified: datetime
    question_id: int


class CreateMultipleChoiceQuestionData(CreateMultipleChoiceQuestionRequest):
    page_id: int
    survey_id: int
    answer_choices: list[ClosedAnswerChoiceRequest]


class MultipleChoiceQuestion(CreateMultipleChoiceQuestionData):
    answer_choices: list[ClosedAnswerChoiceRequest]






