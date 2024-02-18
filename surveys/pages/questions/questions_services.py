from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from surveys.pages.questions.questions_models import Question, CloseEndedAnswerChoice
from surveys.pages.questions.questions_schemas import CreateMultipleChoiceQuestionData, \
    CreateQuestionData, CreateQuestionResponse, ClosedAnswerChoiceRequestData, ClosedAnswerChoice


def create_question(new_question: CreateQuestionData, db: Session) -> CreateQuestionResponse:
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

def create_multi_choice_question_db(new_multi_choice_question: CreateMultipleChoiceQuestionData, db: Session):
    new_question = Question(
        question_text=new_multi_choice_question.question_text,
        question_type=new_multi_choice_question.question_type,
        question_variant=new_multi_choice_question.question_variant,
        page_id=new_multi_choice_question.page_id,
        survey_id=new_multi_choice_question.survey_id,
        date_created=datetime.now(),
        date_modified=datetime.now()
    )

    created_question: CreateQuestionResponse = create_question(new_question, db)

    created_answer_choices: list[ClosedAnswerChoice] = []

    for choice in new_multi_choice_question.answer_choices:
        new_closed_ended_answer_choice = CloseEndedAnswerChoice(
        choice_label = choice.choice_label,
        date_created=datetime.now(),
        date_modified=datetime.now(),
        question_id = created_question.question_id
        )

        created_answer_choices.append(create_multi_choice_question_choice(new_closed_ended_answer_choice, db))

    print(created_answer_choices)



def create_multi_choice_question_choice(choice: ClosedAnswerChoiceRequestData, db: Session) -> ClosedAnswerChoice:
    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice
