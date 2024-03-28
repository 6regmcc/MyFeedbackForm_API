import uuid

from fastapi import APIRouter, status, Request, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from auth.services import get_user_id, check_if_user_has_access_to_survey
from core.database import get_db
from core.security import oauth2_scheme
from responses.responses_data_services import get_table_heading_db
from sqlalchemy.sql import text

router = APIRouter(
    prefix="/responses_data",
    tags=["Responses"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]

)


@router.get("/get_table_headings/{survey_id}")
def get_table_heading(survey_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = get_user_id(request)
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"
        )
    return get_table_heading_db(survey_id=survey_id, db=db)


@router.get('/responses_table_data')
def get_responses_table_data(survey_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = get_user_id(request)
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"
        )
    statement = f"""SELECT   row_to_json(query) from (
	select 
	concat(open_ended_responses.response_id, closed_ended_responses.response_id) as response_id_,
responses.date_created, responses.date_modified, collectors.url as collector_url,
JSON_AGG(json_build_object('choice_id', concat(open_ended_responses.oe_choice_id,closed_ended_responses.ce_choice_id), 'response', concat(open_ended_responses.answer_text ,close_ended_answer_choices.choice_label )))  as responses
FROM questions
left join open_ended_responses
 on questions.question_id = open_ended_responses.question_id
left join closed_ended_responses
	on questions.question_id = closed_ended_responses.question_id
left join open_ended_answer_choices
	on open_ended_responses.oe_choice_id = open_ended_answer_choices.oe_choice_id
left join close_ended_answer_choices
	on closed_ended_responses.ce_choice_id = close_ended_answer_choices.ce_choice_id
left join responses
	on closed_ended_responses.response_id = responses.response_id OR open_ended_responses.response_id = responses.response_id
left join collectors
	on responses.collector_id = collectors.collector_id
	where questions.survey_id = {survey_id}
	group by response_id_, responses.date_created, responses.date_modified, collector_url
) as query
"""
    results_arr = []
    rs = db.scalars(text(statement)).all()
    for row in rs:
        print(row)
        results_arr.append(row)
    return results_arr
