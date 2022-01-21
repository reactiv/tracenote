from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Tweet, UserTweet
from app.schemas.twitter import Tweet as TweetSchema


class TweetCrud:
    def get_multi(
            self, db: Session, user_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[TweetSchema]:
        return db.query(Tweet).join(UserTweet).filter(UserTweet.user_id == user_id)\
                .order_by(desc(Tweet.created_at))\
                .offset(skip).limit(limit).all()

tweet = TweetCrud()
