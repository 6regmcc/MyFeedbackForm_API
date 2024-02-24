from fastapi import APIRouter, status, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.services import check_if_user_has_access_to_survey
from core.database import get_db
from core.security import oauth2_scheme
from surveys.schemas import CreateSurveyRequest, CreateSurveyData, CreateSurveyResponse, Survey, Surveys, \
    SurveyWithPages
from surveys.services import create_survey_db, get_surveys_db, get_survey_db, get_survey_details_db

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


@router.get("", response_model=Surveys)
def get_surveys(request: Request, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    found_surveys = get_surveys_db(owner_id, db)
    survey_arr = []
    for survey in found_surveys:
        survey_arr.append(survey)
    return {"data": survey_arr}


@router.get("/{survey_id}", response_model=SurveyWithPages)
def get_survey(request: Request, survey_id: int, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"
        )
    found_survey = get_survey_db(survey_id=survey_id, db=db)
    if found_survey is None:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )

    return found_survey


@router.get("/{survey_id}/details")
def get_survey_details(request: Request, survey_id: int, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"
        )
    found_survey = get_survey_details_db(survey_id=survey_id, db=db)
    if found_survey is None:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )

    return found_survey
