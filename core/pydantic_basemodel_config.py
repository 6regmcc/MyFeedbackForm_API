from pydantic import BaseModel, ConfigDict


class NoExtraBaseModel(BaseModel):

    model_config = ConfigDict(extra='forbid')
