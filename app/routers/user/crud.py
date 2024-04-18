import os
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models
from . import schemas
from passlib.context import CryptContext
from jose import JWTError,jwt
from dotenv import load_dotenv

load_dotenv('.env/keys.env')

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")



def get_current_user(token:str,db: Session):
    try:
        SecretKey = os.getenv('JWT_SECRET_KEY')
        Algorithm = os.getenv('ALGORITHM')
        payload = jwt.decode(token,SecretKey,algorithms=Algorithm)
        email : str = payload.get('Email')
        username : str = payload.get('UserName')
        id:int=payload.get('id')
        if username is None or email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")
        
        user = get_user_by_email(db=db,Email=email)
        if user:
            return JSONResponse({
                'id':id,
                'UserName':username,
                'Email':email
            })
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")

def get_user_by_email(Email: str,db:Session):
    user = db.query(models.User).filter(models.User.Email == Email).first()
    return user

def create_user(data:schemas.SignUp,db: Session):
    newUser = models.User(UserName=data.UserName,Email=data.Email,
                          Password = pwd_context.hash(data.Password),Location=data.Location,
                          Language=data.Language,UserType = data.UserType,
                          Status=data.Status,Discovered=data.Discovered)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


def create_Access_Token(Email:str,UserName: str):
    encode = {'Email':Email,'UserName':UserName}
    return jwt.encode(encode,JWT_SECRET_KEY,algorithm=ALGORITHM)


def verify_password(enteredpassword,Dbpassword):
    if pwd_context.verify(enteredpassword,Dbpassword):
        return True
    else:
        return False