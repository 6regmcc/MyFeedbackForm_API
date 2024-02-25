from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from surveys.moldels import SurveyModel
from surveys.pages.pages_services import create_page_db, get_list_of_pages_db, get_page_details_db
from surveys.schemas import CreateSurveyData, Survey, SurveyWithPages, SurveyWithPagesDetails
from surveys.pages.pages_models import SurveyPageDB


def create_survey_db(data: CreateSurveyData, db: Session):
    new_survey = SurveyModel(
        survey_name = data.survey_name,
        owner_id = data.owner_id,
        date_created = datetime.now(),
        date_modified = datetime.now()

    )

    db.add(new_survey)
    db.commit()
    db.refresh(new_survey)
    new_page = SurveyPageDB(
        survey_id = new_survey.survey_id
    )
    create_page_db(new_page, db)
    return new_survey


def get_surveys_db(owner_id: int, db: Session):
    query = select(SurveyModel).where(SurveyModel.owner_id == owner_id)
    result = db.scalars(query)
    return result.all()


def get_survey_db(survey_id: int, db: Session) -> SurveyWithPages:
    query = select(SurveyModel).where(SurveyModel.survey_id == survey_id)
    result = db.scalars(query).first()

    pages_arr = get_list_of_pages_db(survey_id=survey_id, db=db)

    survey = SurveyWithPages(
        **result.__dict__,
        pages=pages_arr
    )

    return survey


def get_survey_details_db(survey_id: int, db: Session):
    query = select(SurveyModel).where(SurveyModel.survey_id == survey_id)
    survey = db.scalars(query).first()
    pages_details_arr = []
    pages_arr = get_list_of_pages_db(survey_id=survey_id, db=db)
    for page in pages_arr:
        pages_details_arr.append(get_page_details_db(survey_id=survey_id, page_id=page, db=db))
    del survey._sa_instance_state
    survey_details = SurveyWithPagesDetails(
        **survey.__dict__,
        pages=pages_details_arr
    )

    return survey_details


def delete_survey_db(survey_id: int, db: Session):
    query = select(SurveyModel).where(SurveyModel.survey_id == survey_id)
    found_survey = db.scalars(query).first()
    if found_survey is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find question"
        )
    db.delete(found_survey)
    db.commit()
    deleted_question = {**found_survey.__dict__}
    # del deleted_question._sa_instance_state
    return f"survey deleted: {deleted_question}"

