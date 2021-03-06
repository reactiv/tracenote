from datetime import timedelta
from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/tweets", response_model=schemas.TweetList)
def get_tweets(
    q: str = '',
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    tweets = crud.tweet.get_multi(db, 1, skip=skip, limit=limit, q=q)
    return tweets
