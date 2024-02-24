from fastapi import APIRouter, status, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.services import check_if_user_has_access_to_survey
from core.database import get_db
from core.security import oauth2_scheme
from surveys.pages.questions.questions_schemas import CreateQuestionRequest, CreateQuestionData, \
    CreateMultipleChoiceQuestionRequest, CreateMultipleChoiceQuestionData, CreateOpenEndedQuestionData
from surveys.pages.questions.questions_services import create_multi_choice_question_db, get_question_db, \
    create_open_ended_question_db

router = APIRouter(
    prefix="/surveys/{survey_id}/pages/{page_id}/questions",
    tags=["Surveys"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_question(page_id: int, survey_id: int, create_question_request: CreateQuestionRequest,
                    db: Session = Depends(get_db)):
    if create_question_request.question_type == "closed_ended":
        new_multi_choice_question = CreateMultipleChoiceQuestionData(
            question_text=create_question_request.question_text,
            question_type=create_question_request.question_type,
            question_variant=create_question_request.question_variant,
            page_id=page_id,
            survey_id=survey_id,
            answer_choices=create_question_request.answer_choices
        )

        return create_multi_choice_question_db(new_multi_choice_question, db)

    elif create_question_request.question_type == "open_ended":
        new_open_ended_question = CreateOpenEndedQuestionData(
            **create_question_request.dict(),
            page_id=page_id,
            survey_id=survey_id,

        )

        return create_open_ended_question_db(new_open_ended_question, db)


@router.get("/{question_id}")
def get_question(survey_id: int, page_id: int, question_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )
    found_question = get_question_db(survey_id=survey_id, question_id=question_id, db=db)
    if found_question is None:
        raise HTTPException(
            status_code=404,
            detail="Not found"

        )
    else:
        return found_question


