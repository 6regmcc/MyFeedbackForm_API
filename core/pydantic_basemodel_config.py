from pydantic import BaseModel


class NoExtraBaseModel(BaseModel):
    class Config:
        extra = "forbid"
