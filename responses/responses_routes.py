import uuid


from fastapi import APIRouter, status, Request, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from core.database import get_db
from responses.responses_schemas import SurveyResponseSchema, CreateOrEditResponse
from responses.responses_services import get_survey_page_using_collector_db, create_response_db, \
    create_response_question_db
from surveys.pages.pages_schemas import SurveyPageDetails

router = APIRouter(
    prefix="/responses",
    tags=["Responses"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{collector_url}/{page_number}", response_model=SurveyPageDetails)
def get_survey_form(collector_url: str, page_number: int, response: Response, db: Session = Depends(get_db)):
    #response.set_cookie(key="test_id", value="asdfsdfsd", samesite='none', secure=True,   max_age=10000)
    survey_page = get_survey_page_using_collector_db(collector_url=collector_url, page_number=page_number, db=db)
    return survey_page


@router.post("/{collector_url}/create_response", response_model=SurveyResponseSchema)
def create_response(collector_url: str, db: Session = Depends(get_db)):
    return create_response_db(collector_url=collector_url, db=db)


@router.post("/{collector_url}/create_response/questions/{page_number}")
def create_response_question(collector_url: str, page_number: int, data:CreateOrEditResponse, db: Session = Depends(get_db)):
    return create_response_question_db(collector_url=collector_url, page_number=page_number, data=data,  db=db)