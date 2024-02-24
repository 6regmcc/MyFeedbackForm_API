from fastapi import APIRouter, status, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.services import check_if_user_has_access_to_survey
from core.database import get_db
from core.security import oauth2_scheme
from surveys.pages.pages_schemas import CreatePageRequest, CreatePageData, SurveyPage
from surveys.pages.pages_services import create_page_db, get_page_db, get_page_details_db

router = APIRouter(
    prefix="/surveys/{survey_id}/pages",
    tags=["Surveys"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_page(survey_id: int, data: CreatePageRequest, db: Session = Depends(get_db)):
    new_page = CreatePageData(
        survey_id=survey_id,
        page_title=data.page_title,
        page_description=data.page_description,
    )

    return create_page_db(new_page, db)


@router.get("/{page_id}", response_model=SurveyPage)
def get_page(survey_id: int, page_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )
    found_page = get_page_db(survey_id=survey_id, page_id=page_id, db=db)
    if found_page is None:
        raise HTTPException(
            status_code=404,
            detail="No page found"
        )
    return found_page


@router.get("/{page_id}/details")
def get_page_details(page_id: int, survey_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = request.user.user_id
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )

    found_page_with_details = get_page_details_db(page_id=page_id, survey_id=survey_id, db=db)
    if found_page_with_details is None:
        raise HTTPException(
            status_code=404,
            detail="No page found"
        )

    return found_page_with_details
