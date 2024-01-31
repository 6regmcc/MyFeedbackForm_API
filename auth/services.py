from users.moldels import UserModel
from fastapi.exceptions import HTTPException
from core.security import verify_password

async def get_token(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.username).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return ''


def _get_user_token(user: UserModel, refresh_token = None):
    payload = {"id": user.id}