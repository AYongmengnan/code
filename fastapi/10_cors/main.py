import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response

app = FastAPI()


"""中间件"""
@app.middleware('http')
async def zjj_2(request:Request,call_next):
    # 请求代码块
    print('zjj_2 request')
    response = await call_next(request)
    response.headers['mm'] = 'xixi'
    # 响应代码块
    print('zjj_2 response')
    
    return response

@app.middleware('http')
async def zjj_1(request:Request,call_next):
    # 请求代码块
    print('zjj_1 request')
    # if request.client.host in ['127.0.0.1']:
    #     return Response(content='请24小时后重试')
    print(request.client.host)
    response = await call_next(request)

    # 响应代码块
    print('zjj_1 response')
    
    return response

@app.get('/')
async def get_data():
    print('执行get_data')
    return {
        'meaasges':'data'
    }

@app.get('/item/{item_id}')
async def get_item(item_id:int):
    print('执行get_item')
    return {
        'meaasges':item_id
    }


if __name__ == '__main__':
    uvicorn.run('main:app',port=8050,reload=True,workers=1)