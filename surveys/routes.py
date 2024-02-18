from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import oauth2_scheme
from surveys.schemas import CreateSurveyRequest, CreateSurveyData, CreateSurveyResponse, Survey, Surveys
from surveys.services import create_survey_db, get_surveys_db

router = APIRouter(
    prefix="/surveys",
    tags=["Surveys"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.post("", status_code=status.HTTP_201_CREATED,  response_model=CreateSurveyResponse)
def create_survey(data: CreateSurveyRequest, request: Request, db: Session = Depends(get_db)):
    new_survey = CreateSurveyData(
        survey_name = data.survey_name,
        owner_id = request.user.user_id
    )
    return create_survey_db(new_survey, db)


@router.get("",response_model=Surveys)
def get_surveys(request: Request, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    found_surveys = get_surveys_db(owner_id, db)
    survey_arr = []
    for survey in found_surveys:
        survey_arr.append(survey)
    return {"data": survey_arr}