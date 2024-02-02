from datetime import datetime

from sqlalchemy.orm import Session


from surveys.pages.pages_models import SurveyPage
from surveys.pages.pages_schemas import CreatePageData





def create_page_db(data: CreatePageData, db: Session):
    new_page = SurveyPage(
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