from datetime import datetime
from core.pydantic_basemodel_config import NoExtraBaseModel


from surveys.pages.questions.questions_schemas import OpenEndedQuestion, MultipleChoiceQuestion


class CreatePageRequest(NoExtraBaseModel):
    page_title: str | None = None
    page_description:  str | None = None


class CreatePageData(CreatePageRequest):
    survey_id: int


class CreatePageResponse(CreatePageData):
    page_position: int
    page_id: int
    date_created: datetime
    date_modified: datetime


class SurveyPage(CreatePageResponse):

    questions: list[int]


class SurveyPageDetails(CreatePageResponse):
    survey_name: str
    total_pages: int
    questions: list[OpenEndedQuestion | MultipleChoiceQuestion]


class UpdatePageList(NoExtraBaseModel):
    page_list: list[int]




