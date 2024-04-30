from fastapi import APIRouter
from typing import Union,Optional
from pydantic import BaseModel,Field,validator,EmailStr
from typing import List,Union,Optional
from datetime import date
from fastapi import FastAPI,Form,File,UploadFile,Request
import os
# pip install python-multipart

app07 = APIRouter()

class UserIn(BaseModel):
    username:str
    password:str
    email:EmailStr
    full_name:Union[str,None] = None

class UserOut(BaseModel):
    username:str
    email:EmailStr
    full_name:Union[str,None] = None

class Item(BaseModel):
    name:str
    description:Union[str,None] = None
    price:float
    tax:float=10.5
    tags:List[str] = []

items = {
    'qaz':{'name':'Qaz','price':56.9},
    'wsx':{'name':'Wsx','description':'gfadsfd','price':456.1,'tax':23.6,'tags':['qwer','dfgd']},
    'edc':{'name':'Edc','description':'hgzsDFa','price':46.7,'tax':78.3,'tags':['hnt','okm']}
}

@app07.post('/userinfo',response_model=UserOut)
async def create_user(user:UserIn):
    
    return user

@app07.post('/items/{item_id}',response_model=Item,response_model_exclude_unset=True)
async def create_item(item_id:str):
    return items[item_id]

@app07.post('/items1/{item_id}',response_model=Item,response_model_include={'name'})
async def create_item(item_id:str):
    return items[item_id]
