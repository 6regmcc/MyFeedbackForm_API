from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from users.schemas import CreateUserRequest
from core.database import get_db
from users.services import create_user_account
from core.security import oauth2_scheme
from users.responses import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}}
)

user_router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)




@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data=data, db=db)
    payload = {"message": "User account has been created successfully"}
    return JSONResponse(content=payload)


@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_details(request: Request):
    return request.user