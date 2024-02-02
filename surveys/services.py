from datetime import datetime

from sqlalchemy.orm import Session

from surveys.moldels import SurveyModel
from surveys.pages.pages_services import create_page_db
from surveys.schemas import CreateSurveyData
from surveys.pages.pages_models import SurveyPage


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
    new_page = SurveyPage(
        survey_id = new_survey.survey_id
    )
    create_page_db(new_page, db)
    return new_survey