from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import oauth2_scheme
from surveys.pages.pages_schemas import CreatePageRequest, CreatePageData
from surveys.pages.pages_services import create_page_db

router = APIRouter(
    prefix="/surveys/{survey_id}/pages",
    tags=["Surveys"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("",status_code=status.HTTP_201_CREATED)
def create_page(survey_id: int, data: CreatePageRequest, db: Session = Depends(get_db)):
    new_page = CreatePageData(
        survey_id = survey_id,
        page_title = data.page_title,
        page_description = data.page_description,
    )

    return create_page_db(new_page, db)
