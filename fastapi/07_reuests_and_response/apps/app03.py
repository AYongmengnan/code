from fastapi import APIRouter
from typing import Union,Optional
from pydantic import BaseModel,Field,validator
from typing import List,Union,Optional
from datetime import date
app03 = APIRouter()

class Addr(BaseModel):
    province:Optional[str]
    city:Optional[str]



class User(BaseModel): # 继承BaseModel
    name:str = Field(pattern='^M') # 使用正则必须以大写的M开头
    age:int = Field(default=18,gt=0,lt=100)
    birth:Union[date,None] = None
    friends:List[int] = []
    description:Optional[str]
    addr:Addr

    @validator('name')
    def name_must_alpha(cls,value): # 检查name是否为字母，不是则抛出异常
        assert value.isalpha(),'name is alpha'
        return value

class Data(BaseModel):
    data:List[User]  # 组合嵌套使用

@app03.post('/data')
async def data(data:Data):
    print(data.dict())
    return {
        'data':data
    }


@app03.post('/user')
async def user(user:User):
    # print(user)
    # print(type(user))
    print(user.name)
    print(user.dict())
    return {
        'user_info':user
    }

