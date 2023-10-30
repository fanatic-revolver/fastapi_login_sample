from fastapi import FastAPI,Depends,Header, HTTPException
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
import  models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from enum import Enum
import uvicorn
from typing import Union
from datetime import datetime,timedelta

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str


class Userin(BaseModel):
    username:str
    full_name:str
    email:str
    password:str



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# 配置密码哈希处理上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 配置JWT密钥和算法
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # 模拟的用户数据
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$zj8p3M0Yy4eQ7YdZ0W1j3O7zL6RfN9jGq5g9G3UsXZtCv9uJ0j7q6",  # 密码为password
#         "disabled": False,
#     }
# }

# 创建OAuth2密码Bearer对象
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 创建验证函数，验证用户的用户名和密码是否正确
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# 创建获取用户函数，根据用户名获取用户信息


def get_user(username: str, db: Session =next(get_db())):
        # if username in fake_users_db:
    #     user_dict = fake_users_db[username]
    #     return user_dict
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

@app.post("/createusers")
def createusers(userin:Userin,db: Session = Depends(get_db)):
    new_user=models.User(username=userin.username,full_name=userin.full_name,email=userin.email,hashed_password=get_password_hash(userin.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'data':new_user}


# 创建验证用户函数，根据用户名和密码验证用户
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# 创建生成访问令牌函数，使用用户信息生成JWT令牌
def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 创建登录路由，验证用户名和密码，生成访问令牌
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 创建受保护的路由，需要验证访问令牌
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return {"message": "You are accessing a protected route!"}












if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)


