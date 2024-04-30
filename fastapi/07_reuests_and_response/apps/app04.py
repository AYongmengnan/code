from fastapi import APIRouter
from typing import Union,Optional
from pydantic import BaseModel,Field,validator
from typing import List,Union,Optional
from datetime import date
from fastapi import FastAPI,Form

# pip install python-multipart

app04 = APIRouter()

@app04.post('/regin')
async def reg(username:str=Form(),password:str=Form()):
    print(f'username:{username},password:{password}')
    return {
        'username':username
    }