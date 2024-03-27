from urllib import request

from sqlalchemy.orm import Session

from surveys.routes import get_survey_details
from surveys.services import get_survey_details_db, get_survey_db


def get_table_heading_db(survey_id: int, db: Session):
    found_survey = get_survey_details_db(survey_id=survey_id, db=db)
    column_headers = []
    for page in found_survey.pages:
        for question in page.questions:
            if question.question_type == "closed_ended" and question.question_variant == "multi_choice":
                checkbox_choices_headers = []
                for choice in question.answer_choices:
                    checkbox_choices_header = {
                        "field": str(choice.ce_choice_id),
                        "headerName": choice.choice_label}
                    checkbox_choices_headers.append(checkbox_choices_header)
                checkbox_question_header = {
                    "field": str(question.question_id),
                    "headerName": question.question_text,
                    "children": checkbox_choices_headers
                }
                column_headers.append(checkbox_question_header)
    return column_headers