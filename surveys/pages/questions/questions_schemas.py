from pydantic import BaseModel
from datetime import datetime


class CreateQuestionRequest(BaseModel):
    question_type: str = "closed_ended"
    question_variant: str = "single_choice"
    question_text: str



class CreateQuestionData(CreateQuestionRequest):
    survey_id: int
    page_id: int

class CreateQuestionResponse(CreateQuestionData):
    question_id: int
    date_created: datetime
    date_modified: datetime


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



class CreateMultipleChoiceQuestionData(BaseModel):
    question_type: str = "closed_ended"
    question_variant: str = "single_choice"
    question_text: str
    survey_id: int
    page_id: int
    answer_choices: list[ClosedAnswerChoiceRequest]



class MultipleChoiceQuestion(CreateQuestionResponse):
    answer_choices: list[ClosedAnswerChoice]






