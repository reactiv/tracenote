from typing import Optional, List

from pydantic import BaseModel


class TwitterUser(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class Tweet(BaseModel):
    id: int
    text: str
    author: TwitterUser

    class Config:
        orm_mode = True


class TweetList(BaseModel):
    tweets: List[Tweet]
    total: int
