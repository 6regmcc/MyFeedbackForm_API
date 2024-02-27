from datetime import datetime

from fastapi import APIRouter, status, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.services import check_if_user_has_access_to_survey
from core.database import get_db
from core.security import oauth2_scheme
from surveys.pages.questions.questions_models import CloseEndedAnswerChoice, OpenEndedAnswerChoice
from surveys.pages.questions.questions_schemas import CreateQuestionRequest, CreateQuestionData, \
    CreateMultipleChoiceQuestionRequest, CreateMultipleChoiceQuestionData, CreateOpenEndedQuestionData, \
    CreateQuestionResponse, ClosedAnswerChoiceRequest, \
    OpenEndedAnswerChoiceRequest, ClosedAnswerChoiceRequestData, ClosedAnswerChoiceRequestArr, UpdateChoiceList, \
    UpdateQuestionList
from surveys.pages.questions.questions_services import create_multi_choice_question_db, get_question_db, \
    create_open_ended_question_db, set_question_position, create_multi_choice_question_choice_db, \
    create_open_ended_answer_choice_db, delete_closed_choice_db, delete_open_choice_db, delete_question_db, \
    set_choice_position, update_choice_position, update_question_position_db

router = APIRouter(
    prefix="/surveys/{survey_id}/pages/{page_id}/questions",
    tags=["Questions"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


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


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateQuestionResponse)
def create_question(page_id: int, survey_id: int, create_question_request: CreateQuestionRequest,
                    db: Session = Depends(get_db)):
    if create_question_request.question_type == "closed_ended":
        new_multi_choice_question = CreateMultipleChoiceQuestionData(
            question_text=create_question_request.question_text,
            question_type=create_question_request.question_type,
            question_variant=create_question_request.question_variant,
            question_position=set_question_position(page_id=page_id, db=db),
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
            question_position=set_question_position(page_id=page_id, db=db),

        )

        return create_open_ended_question_db(new_open_ended_question, db)


@router.post("/{question_id}/choices")
def create_answer_choice(survey_id: int, page_id: int, question_id: int,
                         new_ans_choice_request: OpenEndedAnswerChoiceRequest | ClosedAnswerChoiceRequest,
                         request: Request, db: Session = Depends(get_db)):
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
    if isinstance(new_ans_choice_request, ClosedAnswerChoiceRequest) and found_question.question_type == "closed_ended":
        print("this is a closed ended request")
        new_closed_ans_choice = CloseEndedAnswerChoice(
            choice_label=new_ans_choice_request.choice_label,
            date_created=datetime.now(),
            date_modified=datetime.now(),
            choice_position=set_choice_position(question_id=question_id, question_type="closed_ended", db=db),
            question_id=question_id
        )
        return create_multi_choice_question_choice_db(new_closed_ans_choice, db=db)
    elif isinstance(new_ans_choice_request,
                    OpenEndedAnswerChoiceRequest) and found_question.question_type == "open_ended":
        print("this is an open ended request")
        new_open_ans_choice = OpenEndedAnswerChoice(
            choice_label=new_ans_choice_request.choice_label,
            open_ended_choice_type=new_ans_choice_request.open_ended_choice_type,
            date_created=datetime.now(),
            date_modified=datetime.now(),
            choice_position=set_choice_position(question_id=question_id, question_type="open_ended", db=db),
            question_id=question_id
        )
        return create_open_ended_answer_choice_db(new_open_ans_choice, db=db)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Incorrect schema for question type: {found_question.question_type.value}"
        )


@router.delete("/{question_id}")
def delete_question(survey_id: int, page_id: int, question_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )
    return delete_question_db(question_id=question_id, survey_id=survey_id, db=db)


@router.delete("/{question_id}/choices/{choice_id}")
def delete_choice(survey_id: int, question_id: int, choice_id: int, request: Request, db: Session = Depends(get_db)):
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
            detail="Question Not found"

        )

    if found_question.question_type == "closed_ended":
        return delete_closed_choice_db(choice_id=choice_id, db=db)
    elif found_question.question_type == "open_ended":
        return delete_open_choice_db(question_id=question_id, choice_id=choice_id, db=db)
    else:
        return "something went wrong"


@router.patch("/{question_id}/choices/update_position")
def update_answer_choice_position(survey_id: int, question_id, update_choice_list: UpdateChoiceList, request: Request,
                                  db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )
    found_question = get_question_db(survey_id=survey_id, question_id=question_id, db=db)

    return update_choice_position(question_id=question_id,
                                  question_type=found_question.question_type,
                                  choice_list=update_choice_list.choice_list, db=db)


@router.patch("/update_position")
def update_questions_position(survey_id: int, page_id: int, update_question_list: UpdateQuestionList, request: Request, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )

    return update_question_position_db(survey_id=survey_id, page_id=page_id, question_list=update_question_list.question_list, db=db)