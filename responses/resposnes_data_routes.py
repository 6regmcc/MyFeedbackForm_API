import uuid

from fastapi import APIRouter, status, Request, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from auth.services import get_user_id, check_if_user_has_access_to_survey
from core.database import get_db
from core.security import oauth2_scheme
from responses.responses_data_services import get_table_heading_db

router = APIRouter(
    prefix="/responses_data",
    tags=["Responses"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]

)




@router.get("/get_table_headings/{survey_id}")
def get_table_heading(survey_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = get_user_id(request)
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"
        )
    return get_table_heading_db(survey_id=survey_id, db=db)
