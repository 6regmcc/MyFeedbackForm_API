from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from surveys.moldels import SurveyModel
from surveys.pages.pages_services import create_page_db, get_list_of_pages_db
from surveys.schemas import CreateSurveyData, Survey, SurveyWithPages
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
