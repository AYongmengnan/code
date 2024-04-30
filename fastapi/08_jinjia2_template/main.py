from fastapi import FastAPI
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

template = Jinja2Templates(directory='fastapi/08_jinjia2_template/template')

@app.get('/index')
def index(request:Request):
    name = 'qwer'
    email = '1234@qq.com'
    phones = ['123456','199567','183568']
    info = {'age':26,'address':'chongqing'}
    jobs = ['Python','Java','C#','C']
    num_id = 5
    return template.TemplateResponse(
        'index.html', # 模版文件
        {
            'request':request,
            'user':name,
            'email':email,
            'phones':phones,
            'info':info,
            'num_id':num_id,
            'jobs':jobs}
        )

if __name__ == '__main__':
    uvicorn.run('main:app',port=8050,reload=True)