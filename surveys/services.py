import string
from datetime import datetime
import random


from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from responses.responses_models import Collectors
from surveys.moldels import SurveyModel
from surveys.pages.pages_services import create_page_db, get_list_of_pages_db, get_page_details_db
from surveys.schemas import CreateSurveyData, Survey, SurveyWithPages, SurveyWithPagesDetails, CreateSurveyRequest, \
    Collector, CreateCollectorRequest
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
        survey_id = new_survey.survey_id,
        page_title = "",
        page_description = ""
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
    delattr(result, "_sa_instance_state")
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
    delattr(survey, "_sa_instance_state")
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


def update_survey_db(survey_id: int, update_survey_data: CreateSurveyRequest, db: Session):
    query = select(SurveyModel).where(SurveyModel.survey_id == survey_id)
    found_survey = db.scalars(query).first()
    if found_survey is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find question"
        )
    found_survey.survey_name = update_survey_data.survey_name
    found_survey.date_modified = datetime.now()
    db.commit()
    db.refresh(found_survey)
    del found_survey._sa_instance_state
    survey_to_return = Survey(**found_survey.__dict__)

    return survey_to_return


def create_collector_db(survey_id: int, db:Session):
    new_collector = Collectors(
        survey_id=survey_id,
        url=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        is_open=True,
        date_created=datetime.now()
    )
    db.add(new_collector)
    db.commit()
    db.refresh(new_collector)
    del new_collector._sa_instance_state
    return Collector(**new_collector.__dict__)


def get_survey_collectors_db(survey_id: int, db: Session):
    query = select(Collectors).where(Collectors.survey_id == survey_id)
    found_collectors = db.scalars(query).all()
    if found_collectors is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find any survey collectors"
        )
    collector_list = []
    for collector in found_collectors:
        collector_list.append(collector)
    return {"collectors":collector_list}


def get_collector_db(survey_id: int, collector_id: int, db: Session):
    query = select(Collectors).where((Collectors.collector_id == collector_id) & Collectors.survey_id == survey_id)
    found_collector = db.scalar(query)
    del found_collector._sa_instance_state
    return Collector(**found_collector.__dict__)


def update_collector_db(survey_id: int, collector_id: int, data: CreateCollectorRequest, db: Session):
    query = select(Collectors).where((Collectors.survey_id == survey_id) & (Collectors.collector_id == collector_id))
    found_collector = db.scalar(query)
    if found_collector is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find collector"
        )
    found_collector.is_open = data.is_open
    db.commit()
    db.refresh(found_collector)
    del found_collector._sa_instance_state
    return Collector(**found_collector.__dict__)

def delete_collector_db(survey_id: int, collector_id: int, db: Session):
    query = select(Collectors).where((Collectors.survey_id == survey_id) & (Collectors.collector_id == collector_id))
    found_collector = db.scalar(query)
    if found_collector is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find collector"
        )
    db.delete(found_collector)
    db.refresh(found_collector)
    del found_collector._sa_instance_state
    return Collector(**found_collector.__dict__)