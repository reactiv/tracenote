from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import Tweet, UserTweet, TwitterUser
from app.schemas.twitter import Tweet as TweetSchema, TweetList


class TweetCrud:
    def get_multi(
            self, db: Session, user_id: int, *, skip: int = 0, limit: int = 100, q: str = ''
    ) -> TweetList:
        query = db.query(Tweet).join(UserTweet).filter(UserTweet.user_id == user_id)
        if q != '':
            query = query.filter(Tweet.text.ilike(f'%{q.lower()}%'))
        total = query.count()
        results = TweetList(
            tweets=query.order_by(desc(Tweet.created_at)) \
                        .offset(skip).limit(limit).all(),
            total=total
        )
        return results

tweet = TweetCrud()
