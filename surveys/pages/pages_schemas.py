from datetime import datetime

from pydantic import BaseModel

from surveys.pages.questions.questions_schemas import OpenEndedQuestion, MultipleChoiceQuestion


class CreatePageRequest(BaseModel):
    page_title: str | None = None
    page_description:  str | None = None


class CreatePageData(CreatePageRequest):
    survey_id: int


class CreatePageResponse(CreatePageData):
    page_id: int
    date_created: datetime
    date_modified: datetime


class SurveyPage(CreatePageResponse):
    questions: list[int]


class SurveyPageDetails(CreatePageResponse):
    question: list[OpenEndedQuestion | MultipleChoiceQuestion]




