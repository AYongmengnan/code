from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
import uvicorn

app = FastAPI()

# 模拟的用户数据
fake_users_db = {
    "Mark": {
        "username": "Mark",
        "full_name": "Mark Lan",
        "email": "naxidanana@gmail.com",
        "hashed_password": "123456"
    }
}

# 密钥，用于对令牌进行签名
SECRET_KEY = "your_secret_key"

# 访问令牌有效期
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 刷新令牌有效期
REFRESH_TOKEN_EXPIRE_DAYS = 30

# 用户模型
class User(BaseModel):
    username: str
    full_name: str
    email: str
    hashed_password: str

# 生成访问令牌
def create_access_token(username: str):
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expiration_time
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return access_token

# 生成刷新令牌
def create_refresh_token(username: str):
    expiration_time = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": username,
        "exp": expiration_time
    }
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return refresh_token

# 注册新用户
@app.post("/register", response_model=User)
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    # 在实际应用中，您应该对密码进行哈希加密，并存储到数据库中
    fake_users_db[user.username] = user
    return user

# 登录路由
@app.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 在实际应用中，您可以在这里验证用户身份并生成令牌
    username = form_data.username
    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

# 刷新令牌路由
@app.post("/refresh_token", response_model=dict)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        access_token = create_access_token(username)
        return {"access_token": access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

# 受保护的路由，需要验证用户令牌
@app.get("/protected_route", response_model=dict)
async def protected_route(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        return {"message": f"Hello, {username}! This route is protected"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")




if __name__ == '__main__':
    uvicorn.run('main:app',port=8050,reload=True,workers=1)