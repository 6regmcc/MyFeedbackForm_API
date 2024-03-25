from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from responses.responses_models import Collectors
from surveys.moldels import SurveyModel
from surveys.pages.pages_models import SurveyPageDB
from surveys.pages.pages_schemas import SurveyPageDetails
from surveys.pages.pages_services import get_page_details_db


def get_survey_page_using_collector_db(collector_url: str, page_number: int, db: Session) -> SurveyPageDetails:
    survey_id = get_survey_id_from_collector(collector_url=collector_url, db=db)
    page_id = get_page_id_from_position(survey_id=survey_id, page_number=page_number, db=db)

    survey_page = get_page_details_db(survey_id=survey_id, page_id=page_id, db=db)

    return survey_page


def get_survey_id_from_collector(collector_url: str, db: Session) -> int:
    query = select(Collectors.survey_id).where(Collectors.url == collector_url)
    survey_id = db.scalar(query)
    if survey_id is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find survey"
        )
    return survey_id


def get_page_id_from_position(survey_id: int, page_number: int, db: Session) -> int:
    query = select(SurveyPageDB.page_id).where(
        (SurveyPageDB.survey_id == survey_id) & (SurveyPageDB.page_position == page_number))
    page_id = db.scalar(query)
    if page_id is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find survey page"
        )
    return page_id


