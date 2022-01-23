from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


def get_or_create(session, model, value, key="id", **kwargs):
    instance = session.query(model).filter(getattr(model, key) == value).first()
    if instance:
        return instance, False
    else:
        kwargs.update({key: value})
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


class TwitterUser(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50))
    username = Column(String(50))


class Tweet(Base):
    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(BigInteger)
    author_id = Column(BigInteger, ForeignKey('twitter_user.id'))
    author = relationship(TwitterUser)
    text = Column(String(500))
    created_at = Column(DateTime)


class TweetUrl(Base):
    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet, backref="urls")
    short_url = Column(String(100))
    full_url = Column(String(500))


class UserTweet(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)
