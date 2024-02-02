from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import oauth2_scheme
from surveys.schemas import CreateSurveyRequest, CreateSurveyData, CreateSurveyResponse
from surveys.services import create_survey_db

router = APIRouter(
    prefix="/surveys/{survey_id}/pages",
    tags=["Surveys"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("",)
