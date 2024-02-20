from sqlalchemy.orm import Session

from surveys.moldels import SurveyModel
from users.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import verify_password
from core.database import get_setting
from datetime import timedelta
from core.security import create_access_token, create_refresh_token, get_token_payload
from auth.respoonses import TokenResponse
from sqlalchemy import select


settings = get_setting()

async def get_token(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.username).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return await _get_user_token(user=user)

async def get_refresh_token(token, db):
    payload = get_token_payload(token)
    user_id = payload.get("user_id", None)
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return await _get_user_token(user=user, refresh_token=token)


async def _get_user_token(user: UserModel, refresh_token = None):
    payload = {"user_id": user.user_id}
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(payload, access_token_expires)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expires.seconds
    )




def check_if_user_has_access_to_survey(owner_id: int, survey_id: int, db: Session):
    survey = db.query(SurveyModel).filter(SurveyModel.survey_id == survey_id).first()
    if survey is None:
        raise HTTPException(
            status_code=404,
            detail="Not found."
        )
    if survey.owner_id == owner_id:
        return True
    else:
        return False
