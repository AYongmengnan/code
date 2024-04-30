from fastapi import APIRouter

app01 = APIRouter()

@app01.get('/user/1')
async def get_user():
    return {
        'user_id':1,
    }


@app01.get('/user/{user_id}')
async def get_user1(user_id):
    return {
        'user_id':int(user_id) + 1000000,
    }


"""
从上往下依次执行代码，如果查询user_id为1的数据，返回是get_user的结果
如果get_user1在get_user前面返回结果就是1000001
"""