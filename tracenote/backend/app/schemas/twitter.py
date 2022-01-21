from typing import Optional

from pydantic import BaseModel


class Tweet(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True
