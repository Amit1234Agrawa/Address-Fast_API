from sqlalchemy import Column, Integer, String
from .db import Base



class Address(Base):
    '''
        Address Class
    '''
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(String, nullable=False)
    lng = Column(String, nullable=False)