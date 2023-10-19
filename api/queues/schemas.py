from pydantic import BaseModel


class Content(BaseModel):
    text: str
