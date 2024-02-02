from pydantic import BaseModel

class CreatePageRequest(BaseModel):
    page_title: str | None = None
    page_description:  str | None = None


class CreatePageData(CreatePageRequest):
    survey_id: int