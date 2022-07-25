from pydantic import BaseModel
from .db import Base


class Address(BaseModel):
    '''
        BaseModel Address class
    '''
    lat: float
    lng: float

    class Config():
        orm_mode = True


class ShowAddress(BaseModel):
    '''
        BaseModel for ShowAddress Class
    '''
    lat: float
    lng: float

    class Config():
        orm_mode = True