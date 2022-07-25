from fastapi import FastAPI , Depends, HTTPException
from loguru import logger
from . import Schemas, db , models
from .db import engine
from sqlalchemy.orm import Session
import math
import logging 

app = FastAPI()
logger=logging.getLogger(__name__)
logger.setLevel(logging.getLevelName("INFO"))
logging.basicConfig(level=logging.getLevelName("INFO"))


get_db = db.get_db
models.Base.metadata.create_all(engine)

@app.get("/")
def index():
    '''
        Root path for address
    '''
    try:
        return {"Check": "Docs Page"}
    except HTTPException as error:
        logger.error("Root path not found")
        raise error

@app.get("/addresses/")
def get_all(db : Session = Depends(get_db)):
    '''
        To query all address, which are available
    '''
    try:
        address = db.query(models.Address).all()
        if (address==""):
            logger.info("Address is empty")
        return address
    except HTTPException as error:
        logger.error("Error::Address path not found")
        raise error

@app.post('/createaddress/',response_model=Schemas.Address) 
def create_address(request: Schemas.Address,db : Session = Depends(get_db)):
    '''
        Method to create address
    '''
    try:
        new_address = models.Address(**request.dict())
        print(new_address)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        logger.info("Address created successfully")
        return new_address
    except HTTPException as error:
        logger.error("Error::Error occured during creation of Address")
        raise error

@app.get('/addresses/{id}')
def get_address(id: int,db : Session = Depends(get_db)):
    '''
        Method to get particular address using address ID
    '''
    try:
        address = db.query(models.Address).filter(models.Address.id == id).first()
        return address
    except HTTPException as error:
        logger.error(status_code=404, detail=f'Id not {id} not found')
        raise error

@app.delete('/addresses/{id}')
def delete_address(id: int,db : Session = Depends(get_db)):
    '''
        Method to delete address for given ID
    '''
    try:
        address = db.query(models.Address).filter(models.Address.id == id).first()
        db.delete(address)
        db.commit()
        logger.info('Address deleted successfuly')
        return {"message": "Address deleted"}
    except HTTPException as error:
        logger.error(status_code=404, detail=f'Id not {id} not found')
        raise error

@app.put('/addresses/{id}', response_model=Schemas.Address)
def update_address(id: int, request: Schemas.Address,db : Session = Depends(get_db)):
    '''
        Update the address for given address ID
    '''
    try:
        address = db.query(models.Address).filter(models.Address.id == id).first()
        address.lat = request.lat
        address.lng = request.lng
        db.commit()
        logger.info('Address updated successfuly')
        return address
    except HTTPException as error:
        logger.error(status_code=404, detail=f'Id not {id} not found')
        raise error




@app.get('/addresses/{lat}/{lng}/{distance}')
def get_address_by_coordinates(lat: float, lng: float, distance: float, db : Session = Depends(get_db)):
    '''
        Retrieve all the addresses that are from the coordinates to the given distance
    '''
    addresses=[]
    for i in range(361):
        address = db.query(models.Address).filter(models.Address.lat <= float(lat+distance*math.cos(i)), models.Address.lng <= float(lng+distance*math.sin(i))).all()
        addresses.append(address)
    try:
        return addresses
    except HTTPException as error:
        logger.error('Error::Could not fetch address sucessfuly for given coordinates and distance')
        raise error
