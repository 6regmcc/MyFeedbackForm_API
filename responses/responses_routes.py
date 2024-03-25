from fastapi import APIRouter, status, Request, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from core.database import get_db
from responses.responses_services import get_survey_page_using_collector_db
from surveys.pages.pages_schemas import SurveyPageDetails

router = APIRouter(
    prefix="/responses",
    tags=["Responses"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{collector_url}/{page_number}", response_model=SurveyPageDetails)
def get_survey_form(collector_url: str, page_number: int, db: Session = Depends(get_db)):
    survey_page = get_survey_page_using_collector_db(collector_url=collector_url, page_number=page_number, db=db)
    return survey_page
