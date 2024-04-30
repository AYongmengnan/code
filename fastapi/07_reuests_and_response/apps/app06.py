from fastapi import APIRouter
from typing import Union,Optional
from pydantic import BaseModel,Field,validator
from typing import List,Union,Optional
from datetime import date
from fastapi import FastAPI,Form,File,UploadFile,Request
import os
# pip install python-multipart

app06 = APIRouter()

@app06.post('/items')
async def items(request:Request):
    
    return {
        'URL':request.url,
        '请求IP地址':request.client.host,
        'headers':request.headers.get('user-agent'),
        'cookies':request.cookies # 需要postman测试出来
    }
