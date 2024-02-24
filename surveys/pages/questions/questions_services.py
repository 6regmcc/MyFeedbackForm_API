from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from surveys.pages.questions.questions_models import QuestionDB, CloseEndedAnswerChoice, OpenEndedAnswerChoice
from surveys.pages.questions.questions_schemas import CreateMultipleChoiceQuestionData, \
    CreateQuestionData, CreateQuestionResponse, ClosedAnswerChoiceRequestData, ClosedAnswerChoice, \
    MultipleChoiceQuestion, OpenEndedAnswerChoiceRequest, OpenEndedAnswerChoiceResponse, OpenEndedQuestion


def create_question_db(new_question: CreateQuestionData, db: Session) -> CreateQuestionResponse:
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


def create_multi_choice_question_db(new_multi_choice_question: CreateMultipleChoiceQuestionData, db: Session):

    new_question = QuestionDB(
        question_text=new_multi_choice_question.question_text,
        question_type=new_multi_choice_question.question_type,
        question_variant=new_multi_choice_question.question_variant,
        page_id=new_multi_choice_question.page_id,
        survey_id=new_multi_choice_question.survey_id,
        question_position=set_question_position(page_id=new_multi_choice_question.page_id, db=db),
        date_created=datetime.now(),
        date_modified=datetime.now()
    )

    created_question: CreateQuestionResponse = create_question_db(new_question, db)

    created_answer_choices: list[ClosedAnswerChoice] = []

    for choice in new_multi_choice_question.answer_choices:
        new_closed_ended_answer_choice = CloseEndedAnswerChoice(
            choice_label=choice.choice_label,
            date_created=datetime.now(),
            date_modified=datetime.now(),
            question_id=created_question.question_id
        )
        created_choice = create_multi_choice_question_choice_db(new_closed_ended_answer_choice, db)
        created_choice_model = ClosedAnswerChoice(
            choice_label=created_choice.choice_label,
            choice_id=created_choice.choice_id,
            date_created=created_choice.date_created,
            date_modified=created_choice.date_modified
        )
        created_answer_choices.append(created_choice_model)

    create_question_with_choices = MultipleChoiceQuestion(
        question_type=created_question.question_type,
        question_variant=created_question.question_variant,
        question_text=created_question.question_text,
        survey_id=created_question.survey_id,
        page_id=created_question.page_id,
        question_id=created_question.question_id,
        question_position=created_question.question_position,
        date_created=created_question.date_created,
        date_modified=created_question.date_modified,
        answer_choices=created_answer_choices

    )

    return create_question_with_choices


def create_open_ended_question_db(open_ended_question: CreateQuestionData, db: Session):

    new_question = QuestionDB(
        question_text=open_ended_question.question_text,
        question_type=open_ended_question.question_type,
        question_variant=open_ended_question.question_variant,
        page_id=open_ended_question.page_id,
        survey_id=open_ended_question.survey_id,
        question_position=set_question_position(page_id=open_ended_question.page_id, db=db),
        date_created=datetime.now(),
        date_modified=datetime.now()
    )

    created_question: CreateQuestionResponse = create_question_db(new_question, db)

    created_answer_choices: list[OpenEndedAnswerChoiceResponse] = []

    for choice in open_ended_question.answer_choices:
        new_open_ended_answer_choice = OpenEndedAnswerChoice(
            **choice.dict(),
            date_created=datetime.now(),
            date_modified=datetime.now(),
            question_id=created_question.question_id
        )
        created_choice = create_open_ended_answer_choice_db(new_open_ended_answer_choice, db)
        model_created_choice = OpenEndedAnswerChoiceResponse(
            choice_id=created_choice.choice_id,
            question_id=created_choice.question_id,
            open_ended_choice_type=created_choice.open_ended_choice_type,
            choice_label=created_choice.choice_label,
            date_created=created_choice.date_created,
            date_modified=created_choice.date_modified
        )
        created_answer_choices.append(model_created_choice)

    created_question_with_choices = OpenEndedQuestion(
        question_type=created_question.question_type,
        question_variant=created_question.question_variant,
        question_text=created_question.question_text,
        survey_id=created_question.survey_id,
        page_id=created_question.page_id,
        question_id=created_question.question_id,
        question_position=created_question.question_position,
        date_created=created_question.date_created,
        date_modified=created_question.date_modified,
        answer_choices=created_answer_choices
    )

    return created_question_with_choices


def create_multi_choice_question_choice_db(choice: ClosedAnswerChoiceRequestData, db: Session) -> ClosedAnswerChoice:
    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice


def create_open_ended_answer_choice_db(choice: OpenEndedAnswerChoiceRequest,
                                       db: Session) -> OpenEndedAnswerChoiceResponse:
    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice


def get_question_db(survey_id, question_id, db: Session):
    found_question = db.query(QuestionDB).filter(QuestionDB.question_id == question_id).filter(
        QuestionDB.survey_id == survey_id).first()
    print(found_question)
    if found_question is None:
        return None
    if found_question.question_type == "closed_ended":
        return return_multi_choice_question(found_question=found_question, question_id=question_id, db=db)
    elif found_question.question_type == "open_ended":
        return return_open_ended_question(found_question=found_question, question_id=question_id, db=db)


def get_list_of_question_on_page(page_id: int, db: Session) -> list[int]:
    query = select(QuestionDB).where(QuestionDB.page_id == page_id).order_by(QuestionDB.question_position)
    found_questions = db.scalars(query).all()
    question_arr = []
    for question in found_questions:
        question_arr.append(question.question_id)
    return question_arr


def get_question_list_details_db(page_id: int, db: Session):
    query = select(QuestionDB).where(QuestionDB.page_id == page_id).order_by(QuestionDB.question_position)
    found_questions = db.scalars(query).all()
    question_arr = []
    for question in found_questions:
        if question.question_type == "closed_ended":
            question_arr.append(return_multi_choice_question(found_question=question, question_id=question.question_id, db=db))
        elif question.question_type == "open_ended":
            question_arr.append(return_open_ended_question(found_question=question, question_id=question.question_id, db=db))
    return question_arr




def return_multi_choice_question(found_question: QuestionDB, question_id: int, db: Session) -> MultipleChoiceQuestion:
    choices_arr = []
    choices = db.query(CloseEndedAnswerChoice).filter(CloseEndedAnswerChoice.question_id == question_id)
    for choice in choices:
        choices_arr.append(ClosedAnswerChoice(
            choice_id=choice.choice_id,
            date_created=choice.date_created,
            date_modified=choice.date_modified,
            choice_label=choice.choice_label
        ))

    multi_choice_question = MultipleChoiceQuestion(
        question_type=found_question.question_type,
        question_variant=found_question.question_variant,
        question_text=found_question.question_text,
        question_position=found_question.question_position,
        survey_id=found_question.survey_id,
        page_id=found_question.page_id,
        question_id=found_question.question_id,
        date_created=found_question.date_created,
        date_modified=found_question.date_modified,
        answer_choices=choices_arr
    )

    return multi_choice_question


def return_open_ended_question(found_question: QuestionDB, question_id, db):
    choices_arr = []
    query = select(OpenEndedAnswerChoice).where(OpenEndedAnswerChoice.question_id == question_id)
    choices = db.scalars(query).all()
    for choice in choices:
        choices_arr.append(OpenEndedAnswerChoiceResponse(
            choice_id=choice.choice_id,
            open_ended_choice_type=choice.open_ended_choice_type,
            choice_label=choice.choice_label,
            date_created=choice.date_created,
            date_modified=choice.date_modified,
            question_id=choice.question_id
        ))

        open_ended_question = OpenEndedQuestion(
            question_type=found_question.question_type,
            question_variant=found_question.question_variant,
            question_text=found_question.question_text,
            survey_id=found_question.survey_id,
            page_id=found_question.page_id,
            question_id=found_question.question_id,
            date_created=found_question.date_created,
            date_modified=found_question.date_modified,
            question_position=found_question.question_position,
            answer_choices=choices_arr
        )

    return open_ended_question


def set_question_position(page_id: int, db: Session):
    return len(get_list_of_question_on_page(page_id=page_id, db=db)) + 1

