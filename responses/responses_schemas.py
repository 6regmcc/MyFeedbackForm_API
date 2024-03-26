
from datetime import datetime
from uuid import UUID

from core.pydantic_basemodel_config import NoExtraBaseModel






class SurveyResponseSchema(NoExtraBaseModel):
    survey_id: int
    collector_id: int
    session_id: UUID
    response_id: int
    date_created: datetime
    date_modified: datetime


class TypeOfQuestionInfo(NoExtraBaseModel):
    question_type: str = "closed_ended"
    question_variant: str = "single_choice"


class SubmittedResponseMultiChoiceQuestion(NoExtraBaseModel):
    question_id: int
    ce_choice_id: int


class CreateOrEditResponseMultiChoiceQuestion(NoExtraBaseModel):
    question_type: TypeOfQuestionInfo
    submitted_response: SubmittedResponseMultiChoiceQuestion


class CreateOrEditResponse(NoExtraBaseModel):
    session_id: str
    answers: list[CreateOrEditResponseMultiChoiceQuestion]


