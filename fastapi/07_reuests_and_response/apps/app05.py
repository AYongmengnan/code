from fastapi import APIRouter
from typing import Union,Optional
from pydantic import BaseModel,Field,validator
from typing import List,Union,Optional
from datetime import date
from fastapi import FastAPI,Form,File,UploadFile
import os
# pip install python-multipart

app05 = APIRouter()

@app05.post('/file')
async def file(file:bytes=File()):
    # 适合小文件上传
    print('username',file)
    return {
        'file':len(file)
    }

@app05.post('/files')   # 上传多个文件
async def files(files:List[bytes]=File()):
    # 适合小文件上传
    print('username',files)
    return {
        'file':len(files)
    }

@app05.post('/uploadFile')
async def uploadfile(file:UploadFile):
    # 适合大文件上传
    print('username',file.filename)
    path = os.path.join('/code/fastapi/07_reuests_and_response/images',file.filename)
    print(path)
    with open(path,'wb') as f:
        for line in file.file:
            f.write(line)
    return {
        'file':file.filename
    }

@app05.post('/uploadFiles')
async def uploadfiles(files:List[UploadFile]):
    # 适合大文件上传
    # print('username',files.filename)
    files = [file for file in files]
    for file in files:
        path = os.path.join('/code/fastapi/07_reuests_and_response/images',file.filename)
        print(path)
        for file in files:
            with open(path,'wb') as f:
                for line in file.file:
                    f.write(line)
    return {
        'file':[file.filename for file in files]
    }