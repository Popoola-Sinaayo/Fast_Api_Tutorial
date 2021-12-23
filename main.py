from typing import List, Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.sql.functions import mode
from database import SessionLocal
import models

app = FastAPI()

class Items(BaseModel): # This is the serializer similar to the one in django_rest_framework
    id: int
    name: str
    description: str
    price: int
    on_offer: bool = True
    
    class Config:
        orm_mode = True

db = SessionLocal()

@app.get('/items', response_model=List[Items])
async def get_items():
    items = db.query(models.Item).order_by(models.Item.id).all()
    return items

@app.get('/item/{item_id}', response_model=Items)
async def get_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item

@app.post('/items', response_model=Items, status_code=201)
def create_item(item: Items):
    new_item = models.Item(
        id = item.id,
        name = item.name,
        price = item.price,
        description = item.description,
        on_offer = item.on_offer
    )

    new_id = db.query(models.Item).filter(models.Item.id == item.id).first()
    new_name = db.query(models.Item).filter(models.Item.name == item.name).first()
    if new_id and new_name is not None:
        raise HTTPException(status_code=400, detail="Name or id already exist")

    db.add(new_item)
    db.commit()
    return new_item

@app.put('/item/{item_id}', response_model=Items, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: Items):
    item_to_be_updated = db.query(models.Item).filter(models.Item.id==item_id).first()
    item_to_be_updated.id = item.id
    item_to_be_updated.name = item.name
    item_to_be_updated.description = item.description
    item_to_be_updated.price = item.price
    item_to_be_updated.on_offer = item.on_offer
    check_id = db.query(models.Item).filter(models.Item.id==item.id).first()
    check_name = db.query(models.Item).filter(models.Item.name==item.name).first()
    #if check_id and check_name is not None:
    #    raise HTTPException(status_code=400)
    db.commit()
    return item_to_be_updated

@app.delete('/item/{item_id}')
def delete_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id==item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(item_to_delete)
    db.commit()
    return item_to_delete

'''@app.get('/')
def root():
    return {"Hello": "World"}

@app.get('/greet/{name}')
def greet(name: str):
    return {"message": "HEllo " + name}

@app.put('/item/{id}')
def update_item(id: int, item: Items): 
    return {"name": item.name}
    
    # pass in schema to serialize the object
'''