from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from api.student import student
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域的请求，或者指定允许的域名列表
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.include_router(student,prefix='/student',tags=['选课系统学生接口'])

# fast一旦运行，register_tortoise就已执行
register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    
        
)

if __name__ == '__main__':
    uvicorn.run('main:app',port=8050,reload=True,workers=1)