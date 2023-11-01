from sqlalchemy import Column, Integer, String, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

# This file creates the db tables on-the-fly
# so there won't be need to create them in DBMS anymore
# It's a SQL model - it defines how our db table looks likie
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, server_default='TRUE', nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text('now()'))

    user = relationship("User") # based on FK - in order to get user info (e.g. email)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),
                      nullable=False, server_default=text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,
                     ForeignKey("users.id", ondelete="CASCADE"),
                     primary_key=True)
    post_id = Column(Integer,
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     primary_key=True)
