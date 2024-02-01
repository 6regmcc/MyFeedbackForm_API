from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt
from core.config import get_setting

settings = get_setting()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
async def create_access_token(data, expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def create_refresh_token(data):
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

