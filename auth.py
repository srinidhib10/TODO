from fastapi import APIRouter,Depends,HTTPException
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Local
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt, JWTError
import os

router=APIRouter(prefix='/auth',tags=['auth'])
KEY=os.getenv("KEY","4h3g4h3g43h43h4g3h4gh4g3hg434")
algo='HS256'
context=CryptContext(schemes=['bcrypt'],deprecated='auto')
bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class request(BaseModel):
    username:str
    password:str

class token(BaseModel):  
    access_token:str
    token_type:str

def get_db():
    db=Local()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/",status_code=201)
async def create_user(db:db_dependency,cre_req:request):
    if db.query(Users).filter(Users.username==cre_req.username).first():
        raise HTTPException(status_code=400,detail='user already exist')
    user=Users(username=cre_req.username,hashed_pass=context.hash(cre_req.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return{"id":user.id,"username":user.username}

@router.post("/token", response_model=token)
async def login(db:db_dependency, form_data:OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401,detail='Invalid')
    token = create_token(user.username, user.id)
    return {'access_token': token, 'token_type': "bearer"}

def authenticate(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    return user if user and context.verify(password,user.hashed_pass) else None

def create_token(username:str,user_id:int):
    payload={'name':username,'id':user_id}
    return jwt.encode(payload,KEY,algorithm=algo)

def curr_user(token:str=Depends(bearer),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,KEY,algorithms=[algo])
        user=db.query(Users).filter(Users.id==payload.get('id')).first()
        if not user:
            raise HTTPException(status_code=404,detail='user not found')
        return user
    except JWTError:
        raise HTTPException(status_code=401,detail='invalid token')
    


