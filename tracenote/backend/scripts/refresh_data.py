import json
from typing import List

from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.core.data.twitter import TwitterReader
from app.db.base_class import Base
from app.db.init_db import init_db
from app.db.session import engine, SessionLocal
from app.models import User
from app.models.twitter import UserTweet, Tweet, TweetUrl, TwitterUser, get_or_create


def get_initial_user(db: Session) -> User:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
    return user


def load_tweets_from_json(db: Session):
    tweets_json = json.load(open('/Users/jamesgin/tracenote/tracenote/backend/app/notebooks/mytweets.json', 'r'))
    user_tweets = []
    new_users = []
    for tweet in tweets_json:
        author, created = get_or_create(db, TwitterUser, tweet['author_id'])
        if created:
            new_users.append(author)
        urls = [
            TweetUrl(
                short_url=url['url'],
                full_url=url['expanded_url']
            ) for url in tweet.get('entities', {}).get('urls', [])
        ]
        tweet = Tweet(
            tweet_id=tweet['id'],
            text=tweet['text'],
            author=author,
            created_at=tweet['created_at'],
            urls=urls
        )
        user_tweets.append(UserTweet(tweet=tweet))
    add_user_data(new_users)
    return user_tweets


def add_user_data(users: List[TwitterUser]):
    ids = [user.id for user in users]
    reader = TwitterReader()
    twitter_users = reader.get_users(ids)
    data_dict = {t.id: (t.name, t.username) for t in twitter_users}
    for user in users:
        user.name = data_dict[user.id][0]
        user.username = data_dict[user.id][1]


def main():
    try:
        Base.metadata.drop_all(engine)
    except:
        pass

    Base.metadata.create_all(engine)
    db = SessionLocal()
    user = get_initial_user(db)
    user_tweets = load_tweets_from_json(db)
    user.tweets = user_tweets
    db.add(user)
    db.commit()

if __name__ == '__main__':
    main()
