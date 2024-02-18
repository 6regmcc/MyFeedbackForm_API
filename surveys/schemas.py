from pydantic import BaseModel
from datetime import datetime

class CreateSurveyRequest(BaseModel):
    survey_name: str



class CreateSurveyData(CreateSurveyRequest):
    owner_id: int

class CreateSurveyResponse(CreateSurveyData):
    date_created: datetime
    date_modified: datetime
    survey_id: int


class Survey(BaseModel):
    survey_name: str
    date_created: datetime
    date_modified: datetime
    survey_id: int


class Surveys(BaseModel):
    data: list[Survey]