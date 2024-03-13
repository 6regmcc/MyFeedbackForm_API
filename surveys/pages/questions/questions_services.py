from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func, select, delete
from sqlalchemy.orm import Session

from surveys.pages.pages_models import SurveyPageDB
from surveys.pages.questions.questions_models import QuestionDB, CloseEndedAnswerChoice, OpenEndedAnswerChoice
from surveys.pages.questions.questions_schemas import CreateMultipleChoiceQuestionData, \
    CreateQuestionData, CreateQuestionResponse, ClosedAnswerChoiceRequestData, ClosedAnswerChoice, \
    MultipleChoiceQuestion, OpenEndedAnswerChoiceRequest, OpenEndedAnswerChoiceResponse, OpenEndedQuestion, \
    ClosedAnswerChoiceRequest, UpdateQuestionRequest, UpdateOpenEndedAnswerChoice


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

    for index, choice in enumerate(new_multi_choice_question.answer_choices):
        new_closed_ended_answer_choice = CloseEndedAnswerChoice(
            choice_label=choice.choice_label,
            date_created=datetime.now(),
            date_modified=datetime.now(),
            choice_position= index +  1,
            question_id=created_question.question_id
        )
        created_choice = create_multi_choice_question_choice_db(new_closed_ended_answer_choice, db)
        created_choice_model = ClosedAnswerChoice(
            choice_label=created_choice.choice_label,
            ce_choice_id=created_choice.ce_choice_id,
            date_created=created_choice.date_created,
            choice_position=created_choice.choice_position,
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

    for index, choice in enumerate(open_ended_question.answer_choices):
        new_open_ended_answer_choice = OpenEndedAnswerChoice(
            open_ended_choice_type=choice.open_ended_choice_type,
            choice_label=choice.choice_label,
            date_created=datetime.now(),
            date_modified=datetime.now(),
            question_id=created_question.question_id,
            choice_position=index+1
        )
        created_choice = create_open_ended_answer_choice_db(new_open_ended_answer_choice, db)
        model_created_choice = OpenEndedAnswerChoiceResponse(
            oe_choice_id=created_choice.oe_choice_id,
            question_id=created_choice.question_id,
            open_ended_choice_type=created_choice.open_ended_choice_type,
            choice_label=created_choice.choice_label,
            date_created=created_choice.date_created,
            choice_position=created_choice.choice_position,
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


def create_multi_choice_question_choice_db(choice: CloseEndedAnswerChoice, db: Session) -> ClosedAnswerChoice:
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


def get_question_list_details_db(page_id: int,survey_id: int, db: Session):
    query = select(QuestionDB).where((QuestionDB.page_id == page_id) & (QuestionDB.survey_id == survey_id)).order_by(QuestionDB.question_position)
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
            ce_choice_id=choice.ce_choice_id,
            date_created=choice.date_created,
            date_modified=choice.date_modified,
            choice_label=choice.choice_label,
            choice_position=choice.choice_position
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
            oe_choice_id=choice.oe_choice_id,
            open_ended_choice_type=choice.open_ended_choice_type,
            choice_label=choice.choice_label,
            date_created=choice.date_created,
            date_modified=choice.date_modified,
            choice_position=choice.choice_position,
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


def delete_closed_choice_db(choice_id: int, db: Session):
    query = db.get(CloseEndedAnswerChoice, choice_id)
    if query is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find answer choice"
        )
    db.delete(query)
    db.commit()
    return "choice deleted"


def delete_open_choice_db(question_id: int, choice_id: int, db: Session):
    query = db.get(OpenEndedAnswerChoice, choice_id)
    if query is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find answer choice"
        )
    db.delete(query)
    db.commit()
    choice_list = get_list_of_oe_choices(question_id, db=db)
    update_choices = update_choice_position(question_id=question_id, question_type="open_ended", choice_list=choice_list, db=db)
    if not update_choices == "choice list successfully updated":
        return "something went wrong"
    return "choice deleted"


def delete_question_db(question_id: int, survey_id: int, page_id: int, db: Session):

    query = select(QuestionDB).where((QuestionDB.question_id == question_id) & (QuestionDB.survey_id == survey_id))
    found_question = db.scalars(query).first()
    if found_question is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find question"
        )
    db.delete(found_question)
    db.commit()
    deleted_question = {**found_question.__dict__}
    question_list = get_list_of_question_on_page(page_id=page_id, db=db)
    updated_questions_position = update_question_position_db(survey_id=survey_id,page_id=page_id, question_list=question_list, db=db)
    if updated_questions_position is None:
        raise HTTPException(
            status_code=500,
            detail="There was a problem updating question position after delete"
        )
    return f"question deleted: {deleted_question}"


def get_list_of_ce_choices(question_id: int, db: Session) -> list[int]:
    query = select(CloseEndedAnswerChoice).where(CloseEndedAnswerChoice.question_id == question_id).order_by(CloseEndedAnswerChoice.choice_position)
    found_choices = db.scalars(query).all()
    choice_arr = []
    for choice in found_choices:
        choice_arr.append(choice.ce_choice_id)
    return choice_arr


def get_list_of_oe_choices(question_id: int, db: Session) -> list[int]:
    query = select(OpenEndedAnswerChoice).where(OpenEndedAnswerChoice.question_id == question_id).order_by(OpenEndedAnswerChoice.choice_position)
    found_choices = db.scalars(query).all()
    choice_arr = []
    for choice in found_choices:
        choice_arr.append(choice.oe_choice_id)
    return choice_arr


def set_choice_position(question_id: int, question_type:str, db: Session):

    if question_type == "open_ended":
        return len(get_list_of_oe_choices(question_id=question_id, db=db)) + 1
    elif question_type == "closed_ended":
        return len(get_list_of_ce_choices(question_id=question_id, db=db)) + 1


def update_choice_position(question_id: int, question_type: str, choice_list: list[int], db: Session):
    if question_type == "closed_ended":
        if len(choice_list) != len(get_list_of_ce_choices(question_id=question_id, db=db)):
            return "choice list incorrect length"
        for index, choice in enumerate(choice_list):
            query = select(CloseEndedAnswerChoice).where((CloseEndedAnswerChoice.ce_choice_id == choice) & (CloseEndedAnswerChoice.question_id == question_id))
            found_choice = db.scalars(query).first()
            if found_choice is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Unable to find answer choice_id: {choice}"
                )
            found_choice.choice_position = index + 1
            db.commit()

        updated_choice_position = get_list_of_ce_choices(question_id=question_id, db=db)

        if updated_choice_position == choice_list:
            return "choice list successfully updated"
        else:
            return "something went wrong."

    if question_type == "open_ended":
        if len(choice_list) != len(get_list_of_oe_choices(question_id=question_id, db=db)):
            return "choice list incorrect length"
        for index, choice in enumerate(choice_list):
            query = select(OpenEndedAnswerChoice).where((OpenEndedAnswerChoice.oe_choice_id == choice) & (OpenEndedAnswerChoice.question_id == question_id))
            found_choice = db.scalars(query).first()
            if found_choice is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Unable to find answer choice_id: {choice}"
                )
            found_choice.choice_position = index + 1
            db.commit()

        updated_choice_position = get_list_of_oe_choices(question_id=question_id, db=db)
        if updated_choice_position == choice_list:
            return "choice list successfully updated"
        else:
            return "something went wrong."


def update_question_position_db(survey_id: int, page_id: int, question_list: list[int], db: Session):
    query = select(SurveyPageDB).where((SurveyPageDB.survey_id == survey_id) & (SurveyPageDB.page_id == page_id))
    found_page = db.scalar(query)
    if found_page is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find survey page"
        )
    if len(question_list) != len(get_list_of_question_on_page(page_id=found_page.page_id, db=db)):
        return "incorrect question_id list length"

    for index, question in enumerate(question_list):
        query = select(QuestionDB).where((QuestionDB.page_id == page_id) & (QuestionDB.survey_id == survey_id) & (QuestionDB.question_id == question))
        found_question = db.scalar(query)
        if found_question is None:
            raise HTTPException(
                status_code=404,
                detail="Unable to find question"
            )
        found_question.question_position = index + 1
        db.commit()

    updated_question_list = get_list_of_question_on_page(page_id=found_page.page_id, db=db)
    if updated_question_list == question_list:
        return "question position successfully updated"
    else:
        return "something went wrong"


def update_question_db(survey_id: int, page_id: int, question_id: int, update_question_data: UpdateQuestionRequest, db: Session):
    query = select(QuestionDB).where((QuestionDB.survey_id == survey_id) & (QuestionDB.page_id == page_id) & (QuestionDB.question_id == question_id))
    found_question: QuestionDB = db.scalar(query)
    if found_question is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find question"
        )
    found_question.question_text = update_question_data.question_text
    found_question.date_modified = datetime.now()
    db.commit()
    db.refresh(found_question)

    return get_question_db(survey_id=survey_id, question_id=question_id, db=db)


def get_question_type(survey_id: int, page_id: int, question_id: int, db: Session):
    query = select(QuestionDB).where((QuestionDB.survey_id == survey_id) & (QuestionDB.page_id == page_id) & (QuestionDB.question_id == question_id))
    found_question = db.scalar(query)
    if found_question is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find question"
        )
    return found_question.question_type


def update_answer_choice_db(survey_id: int, page_id: int, question_id: int, choice_id: int, update_choice_data: UpdateOpenEndedAnswerChoice, db: Session):
    question_type = get_question_type(survey_id=survey_id, page_id=page_id, question_id=question_id, db=db)
    if question_type == "open_ended":
        return update_open_ended_answer_choice(choice_id=choice_id, update_choice_data=update_choice_data, db=db)


def update_open_ended_answer_choice(choice_id: int, update_choice_data: UpdateOpenEndedAnswerChoice, db: Session):
    query = select(OpenEndedAnswerChoice).where(OpenEndedAnswerChoice.oe_choice_id == choice_id)
    found_choice: OpenEndedAnswerChoice = db.scalar(query)
    if found_choice is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to find answer choice"
        )

    found_choice.choice_label = update_choice_data.choice_label
    found_choice.date_modified = datetime.now()
    db.commit()
    db.refresh(found_choice)
    del found_choice._sa_instance_state
    return OpenEndedAnswerChoiceResponse(**found_choice.__dict__)




