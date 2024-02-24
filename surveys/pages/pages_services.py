from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session


from surveys.pages.pages_models import SurveyPageDB
from surveys.pages.pages_schemas import CreatePageData, SurveyPage
from surveys.pages.questions.questions_services import get_list_of_question_on_page, get_question_list_details_db


#add return type
def create_page_db(data: CreatePageData, db: Session):
    new_page = SurveyPageDB(
        page_title=data.page_title,
        page_description=data.page_description,
        survey_id=data.survey_id,
        date_created=datetime.now(),
        date_modified=datetime.now()
    )

    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return new_page


def get_page_db(survey_id: int, page_id: int, db: Session) -> SurveyPage:
    page_query = select(SurveyPageDB).where(SurveyPageDB.survey_id == survey_id).where(SurveyPageDB.page_id == page_id)
    page = db.scalars(page_query).first()
    if page is None:
        return None
    question_list = get_list_of_question_on_page(page_id=page.page_id, db=db)
    survey_page = SurveyPage(
        **page.__dict__,
        questions=question_list
    )

    return survey_page


def get_page_details_db(survey_id: int, page_id: int, db: Session):
    page_query = select(SurveyPageDB).where(SurveyPageDB.survey_id == survey_id).where(SurveyPageDB.page_id == page_id)
    page = db.scalars(page_query).first()
    if page is None:
        return None
    question_list = get_question_list_details_db(page_id=page.page_id, db=db)
    survey_page = SurveyPage(
        **page.__dict__,
        questions=question_list
    )