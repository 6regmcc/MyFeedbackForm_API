import uuid
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from responses.responses_models import Collectors, SurveyResponse, ClosedEndedResponses
from responses.responses_schemas import CreateOrEditResponse
from surveys.moldels import SurveyModel
from surveys.pages.pages_models import SurveyPageDB
from surveys.pages.pages_schemas import SurveyPageDetails
from surveys.pages.pages_services import get_page_details_db


def get_survey_page_using_collector_db(collector_url: str, page_number: int, db: Session) -> SurveyPageDetails:
    survey_id = get_collector_from_collector_url(collector_url=collector_url, db=db).survey_id
    page_id = get_page_id_from_position(survey_id=survey_id, page_number=page_number, db=db)

    survey_page = get_page_details_db(survey_id=survey_id, page_id=page_id, db=db)

    return survey_page


def get_collector_from_collector_url(collector_url: str, db: Session):
    query = select(Collectors).where(Collectors.url == collector_url)
    collector = db.scalar(query)
    if collector is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find survey"
        )
    return collector


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


def create_response_db(collector_url: str, db: Session):
    found_collector = get_collector_from_collector_url(collector_url=collector_url, db=db)
    new_response = SurveyResponse(

        survey_id=found_collector.survey_id,
        collector_id=found_collector.collector_id,
        session_id=uuid.uuid4(),
        date_created=datetime.now(),
        date_modified=datetime.now()
    )
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response


def create_response_question_db(collector_url, page_number, data: CreateOrEditResponse, db):
    found_collector = get_collector_from_collector_url(collector_url=collector_url, db=db)
    query = select(SurveyResponse).where(SurveyResponse.collector_id == found_collector.collector_id)
    found_response = db.scalar(query)

    if found_response is None and page_number == 1:
        print('create new response')
        new_response_db = SurveyResponse(

            survey_id=found_collector.survey_id,
            collector_id=found_collector.collector_id,
            session_id=uuid.UUID(data.session_id).hex,
            date_created=datetime.now(),
            date_modified=datetime.now()
        )
        db.add(new_response_db)
        db.commit()
        found_response = new_response_db
    if found_response is None and page_number > 1:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. go back to ppage 1"
        )
    saved_question_responses = []
    for question in data.answers:
        if question.question_type.question_type == "closed_ended" and question.question_type.question_variant == "single_choice":
            new_ce_response = save_or_update_multi_choice_question(response_id=found_response.response_id, question_id=question.submitted_response.question_id, ce_choice_id=question.submitted_response.ce_choice_id, db=db)
            saved_question_responses.append(new_ce_response)
    return {
        "response_id": found_response.response_id,
        "collector_id": found_response.collector_id,
        "session_id": str(found_response.session_id),
        "date_created": found_response.date_created,
        "date_modified": found_response.date_modified,
        "answers": saved_question_responses
    }

def save_or_update_multi_choice_question(response_id, question_id, ce_choice_id, db: Session):
    query = select(ClosedEndedResponses).where((ClosedEndedResponses.response_id == response_id) & (ClosedEndedResponses.question_id == question_id) & (ClosedEndedResponses.ce_choice_id == ce_choice_id))
    found_response = db.scalar(query)
    if found_response:
        print('ce response found')
        db.delete(found_response)
        db.commit()
    new_ce_response = ClosedEndedResponses(
        response_id=response_id,
        question_id=question_id,
        ce_choice_id=ce_choice_id
    )
    db.add(new_ce_response)
    db.commit()
    db.refresh(new_ce_response)
    return new_ce_response

