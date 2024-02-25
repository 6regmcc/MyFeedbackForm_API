from core.pydantic_basemodel_config import NoExtraBaseModel

from datetime import datetime


class CreateSurveyRequest(NoExtraBaseModel):
    survey_name: str


class CreateSurveyData(CreateSurveyRequest):
    owner_id: int


class CreateSurveyResponse(CreateSurveyData):
    date_created: datetime
    date_modified: datetime
    survey_id: int


class Survey(NoExtraBaseModel):
    survey_name: str
    date_created: datetime
    date_modified: datetime
    survey_id: int


class Surveys(NoExtraBaseModel):
    data: list[Survey]


class SurveyWithPages(Survey):
    pages: list[int]


class SurveyWithPagesDetails(Survey):
    pages: list
