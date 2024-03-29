from fastapi import APIRouter, status, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.services import check_if_user_has_access_to_survey, get_user_id
from core.database import get_db
from core.security import oauth2_scheme
from surveys.pages.pages_schemas import CreatePageRequest, CreatePageData, SurveyPage, UpdatePageList, \
    CreatePageResponse
from surveys.pages.pages_services import create_page_db, get_page_db, get_page_details_db, delete_page_db, \
    update_page_position_db, update_page_db
from surveys.pages.questions.questions_services import update_question_position_db



router = APIRouter(
    prefix="/surveys/{survey_id}/pages",
    tags=["Pages"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_page(survey_id: int, data: CreatePageRequest, request: Request, db: Session = Depends(get_db)):
    owner_id = get_user_id(request)
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )
    new_page = CreatePageData(
        survey_id=survey_id,
        page_title=data.page_title,
        page_description=data.page_description,
    )

    return create_page_db(new_page, db)


@router.get("/{page_id}", response_model=SurveyPage)
def get_page(survey_id: int, page_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = get_user_id(request)
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
    owner_id = get_user_id(request)
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


@router.delete("/{page_id}")
def delete_page(page_id: int, survey_id: int, request: Request, db: Session = Depends(get_db)):
    owner_id = get_user_id(request)
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )
    return delete_page_db(survey_id=survey_id, page_id=page_id, db=db)


@router.patch("/update_position")
def update_page_position(survey_id: int, page_list: UpdatePageList, request: Request, db: Session = Depends(get_db)):
    owner_id = get_user_id(request)
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"

        )
    return update_page_position_db(survey_id=survey_id, page_list=page_list.page_list, db=db)


@router.put("/{page_id}" , response_model=CreatePageResponse)
def update_page(survey_id: int, page_id: int, update_page_data: CreatePageRequest,  request: Request, db: Session = Depends(get_db)):
    owner_id = get_user_id(request)
    if not check_if_user_has_access_to_survey(owner_id=owner_id, survey_id=survey_id, db=db):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this resource"
        )
    return update_page_db(survey_id=survey_id, page_id=page_id, update_page_data=update_page_data, db=db)