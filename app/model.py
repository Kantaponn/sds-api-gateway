from pydantic import BaseModel


class MessageError(BaseModel):
    error: str
