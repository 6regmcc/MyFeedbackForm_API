from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import oauth2_scheme
from surveys.pages.questions.questions_schemas import CreateQuestionRequest, CreateQuestionData, CreateMultipleChoiceQuestionRequest, CreateMultipleChoiceQuestionData
from surveys.pages.questions.questions_services import create_multi_choice_question_db

router = APIRouter(
    prefix="/surveys/{survey_id}/pages/{page_id}/questions",
    tags=["Surveys"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_question(page_id: int, survey_id: int, create_question_request: CreateMultipleChoiceQuestionRequest, db: Session = Depends(get_db)):
    if create_question_request.question_type == "closed_ended":
        new_multi_choice_question = CreateMultipleChoiceQuestionData(
            question_text = create_question_request.question_text,
            question_type = create_question_request.question_type,
            question_variant = create_question_request.question_variant,
            page_id = page_id,
            survey_id = survey_id,
            answer_choices = create_question_request.answer_choices
        )

        return create_multi_choice_question_db(new_multi_choice_question, db)
