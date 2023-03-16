from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String

Base = declarative_base()

class Account(Base):
    __tablename__='account'
    id = Column(Integer, primary_key=True)
    email = Column(String(20))
    username = Column(String(20))
    password = Column(String(20))
