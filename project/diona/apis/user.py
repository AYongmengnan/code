from fastapi import APIRouter, Request
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from models import User

user = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 密钥，用于对令牌进行签名
SECRET_KEY = "diona"

# 访问令牌有效期
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 刷新令牌有效期
REFRESH_TOKEN_EXPIRE_DAYS = 30

# 用户模型
class CreateUser(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str] = None
    password: Optional[str]

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
@user.post("/register", response_model=CreateUser)
async def register(user: CreateUser):
    u_data = await User.filter(name=user.name)
    if u_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    # 在实际应用中，您应该对密码进行哈希加密，并存储到数据库中
    password = user.password
    hashed_password = pwd_context.hash(password)
    await User.create(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hashed_password
        )
    return user

# 登录路由
@user.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 检查用户是否存在
    user_data = await User.filter(email=form_data.username).first()
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    # 验证密码
    if not pwd_context.verify(form_data.password, user_data.password):
        print(form_data.password)
        print(user_data.password)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # 生成访问令牌和刷新令牌
    access_token = create_access_token(form_data.username)
    refresh_token = create_refresh_token(form_data.username)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
# 刷新令牌路由
@user.post("/refresh_token", response_model=dict)
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

# # 受保护的路由，需要验证用户令牌
# @user.get("/info", response_model=dict)
# async def protected_route(token: str = Depends(OAuth2PasswordBearer(tokenUrl="login"))):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         username = payload.get("sub")
#         return {"message": f"Hello, {username}! This route is protected"}
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        # 在这里可以根据用户名从数据库中获取用户信息，或者进行其他操作
        # 这里简单返回用户名作为当前用户信息
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# 在需要验证用户访问令牌的路由中使用 get_current_user 依赖函数
@user.get("/info", response_model=dict)
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! This route is protected"}

