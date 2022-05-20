import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), unique=True)
    author = Column(String(250), unique=False)
    genre = Column(String(250))


engine = create_engine('sqlite:///home_library.db')

Base.metadata.create_all(engine)