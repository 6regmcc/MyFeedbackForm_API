from pydantic import EmailStr

from core.pydantic_basemodel_config import NoExtraBaseModel


class CreateUserRequest(NoExtraBaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

