import time
from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from huakuai import generate_random_string,hk_yzm

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域的请求，或者指定允许的域名列表
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get('/yzm')
async def yzm():
    # keyword = generate_random_string()
    # res = hk_yzm(keyword)
    # return {
    #     'msg':res
    # }
    time.sleep(8)
    return {'test':'test'}

if __name__ == '__main__':
    uvicorn.run('main:app',port=8050,reload=True,workers=1)