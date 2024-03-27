
from datetime import datetime
from uuid import UUID

from core.pydantic_basemodel_config import NoExtraBaseModel






class SurveyResponseSchema(NoExtraBaseModel):
    survey_id: int
    collector_id: int
    session_id: str
    response_id: int
    date_created: datetime
    date_modified: datetime


class MultiChoiceQuestionTypeInfo(NoExtraBaseModel):
    question_type: str = "closed_ended"
    question_variant: str = "single_choice"


class CheckboxQuestionTypeInfo(NoExtraBaseModel):
    question_type: str = "closed_ended"
    question_variant: str = "multi_choice"


class SubmittedResponseMultiChoiceQuestion(NoExtraBaseModel):
    question_id: int
    ce_choice_id: int


class SubmittedCheckboxQuestion(NoExtraBaseModel):
    question_id: int
    ce_choices: list[int]


class CreateOrEditResponseCeChoiceQuestion(NoExtraBaseModel):
    question_type: MultiChoiceQuestionTypeInfo | CheckboxQuestionTypeInfo
    submitted_response: SubmittedResponseMultiChoiceQuestion | SubmittedCheckboxQuestion



class CreateOrEditResponse(NoExtraBaseModel):
    session_id: str
    answers: list[CreateOrEditResponseCeChoiceQuestion]


class MultiChoiceResponseAnswers(NoExtraBaseModel):
    ce_choice_id: int
    question_id: int
    response_id: int


class CheckboxResponseAnswers(NoExtraBaseModel):
    question_id: int
    response_id: int
    ce_choices: list[int]


class SurveyResponseWithAnswers(NoExtraBaseModel):
    response_id: int
    collector_id: int
    session_id: str
    date_created: datetime
    date_modified: datetime
    answers: list[MultiChoiceResponseAnswers| CheckboxResponseAnswers]