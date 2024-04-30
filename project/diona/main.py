from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from apis.user import user
from apis.animes import anime
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域的请求，或者指定允许的域名列表
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
)
# app.include_router(user,prefix='/user',tags=['用户相关接口'])
app.include_router(anime,prefix='/anime',tags=['动漫相关接口'])

if __name__ == "__main__":
    uvicorn.run('main:app',port=8055,reload=True,workers=1)