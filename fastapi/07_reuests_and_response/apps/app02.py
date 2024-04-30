from fastapi import APIRouter
from typing import Union,Optional
app02 = APIRouter()

@app02.get('/jobs')
async def get_jobs(kd,xl,gj):
    return {
        'msg':{
            '关键字':kd,
            '学历':xl,
            '工作经验':gj
        }
    }

# @app02.get('/jobs/{kd}')  # 路径参数与查询参数都存在
# async def get_jobs(kd,xl,gj):
#     return {
#         'msg':{
#             '关键字':kd,
#             '学历':xl,
#             '工作经验':gj,
#         }
#     }

@app02.get('/jobs/{kd}')  # 路径参数与查询参数都存在,且设置部分参数不是必填参数
async def get_jobs(kd,xl:Union[str,None] = None,gj:Optional[str]=None): # Union多种类型选择，后面 = 赋予默认值
    return {
        'msg':{
            '关键字':kd,
            '学历':xl,
            '工作经验':gj,
        }
    }