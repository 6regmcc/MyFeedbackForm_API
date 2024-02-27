from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


from surveys.pages.pages_models import SurveyPageDB
from surveys.pages.pages_schemas import CreatePageData, SurveyPage, SurveyPageDetails
from surveys.pages.questions.questions_services import get_list_of_question_on_page, get_question_list_details_db


#add return type
def create_page_db(data: CreatePageData, db: Session):
    new_page = SurveyPageDB(
        page_title=data.page_title,
        page_description=data.page_description,
        survey_id=data.survey_id,
        page_position=set_page_position(data.survey_id, db=db),
        date_created=datetime.now(),
        date_modified=datetime.now()
    )

    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return new_page


def get_page_db(survey_id: int, page_id: int, db: Session):
    page_query = select(SurveyPageDB).where(SurveyPageDB.survey_id == survey_id).where(SurveyPageDB.page_id == page_id)
    page = db.scalars(page_query).first()
    if page is None:
        return None
    question_list = get_list_of_question_on_page(page_id=page.page_id, db=db)
    del page._sa_instance_state
    survey_page = SurveyPage(
        **page.__dict__,
        questions=question_list
    )

    return survey_page


def get_page_details_db(survey_id: int, page_id: int, db: Session):
    page_query = select(SurveyPageDB).where((SurveyPageDB.survey_id == survey_id) & (SurveyPageDB.page_id == page_id)).order_by(SurveyPageDB.page_position)
    page = db.scalars(page_query).first()
    if page is None:
        return None
    question_list = get_question_list_details_db(page_id=page.page_id, survey_id=survey_id, db=db)
    del page._sa_instance_state
    survey_page = SurveyPageDetails(
        **page.__dict__,

        questions=question_list
    )

    return survey_page


def get_list_of_pages_db(survey_id: int, db: Session) -> list[int]:
    query = select(SurveyPageDB).where(SurveyPageDB.survey_id == survey_id).order_by(SurveyPageDB.page_position)
    found_pages = db.scalars(query).all()
    page_arr = []
    for page in found_pages:
        page_arr.append(page.page_id)
    return page_arr


def set_page_position(survey_id: int, db: Session):
    return len(get_list_of_pages_db(survey_id=survey_id, db=db)) + 1


def delete_page_db(survey_id: int, page_id: int, db: Session):
    query = db.get(SurveyPageDB, page_id)
    if query is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find question"
        )
    db.delete(query)
    db.commit()
    deleted_page = {**query.__dict__}
    # del deleted_question._sa_instance_state
    return f"question page: {deleted_page}"
