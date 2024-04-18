from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from app.routers.user import crud, schemas
from app.database import get_db
from fastapi.responses import JSONResponse


router = APIRouter(
    tags = ['User'],
    prefix='/User'
)


@router.post('/SignUp')
async def create(data:schemas.SignUp,db:Session = Depends(get_db)):
    user = crud.get_user_by_email(Email=data.Email,db=db)
    if user:
        return {'detail':'User already created',
                'status_code':status.HTTP_406_NOT_ACCEPTABLE}
    else:
        newuser = crud.create_user(data=data,db=db)
        accessToken = crud.create_Access_Token(Email=newuser.Email,UserName=newuser.UserName)
        return JSONResponse({
            'detail':{
                'AccessToken':accessToken,
                'UserId':newuser.Id,
                'UserEmail':newuser.Email
            },
            'status_code':status.HTTP_200_OK
        })

@router.post('/LogIn')
async def login(data:schemas.LogIn,db: Session=Depends(get_db)):
    checkUser = crud.get_user_by_email(Email=data.Email,db=db)
    if checkUser:
        verifyPassword = crud.verify_password(enteredpassword=data.Password,Dbpassword=checkUser.Password)
        if verifyPassword == True:
            accessToken = crud.create_Access_Token(checkUser.Email,checkUser.UserName)
            return JSONResponse({
                'detail':{
                    'AccessToken':accessToken,
                    'UserId':checkUser.Id,
                    'UserEmail':checkUser.Email
                },
                'status_code':status.HTTP_200_OK
            })
        else:
            return HTTPException(detail='Password Incorrect',status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return HTTPException(detail='Invalid Email',status_code=status.HTTP_401_UNAUTHORIZED)
    
@router.put('/Change-Password')
async def changepassword(data:schemas.ChangePassword,db:Session = Depends(get_db)):
    checkUser = crud.get_user_by_email(Email=data.Email,db=db)
    if checkUser:
        verifyPassword = crud.verify_password(enteredpassword=data.OldPassword,Dbpassword=checkUser.Password)
        if verifyPassword == True:
            checkUser.Password = crud.pwd_context.hash(checkUser.Password)
            db.commit()
            return {'detail':'Updated Password Successfully',
                    'status_code':status.HTTP_200_OK}
        else:
            return {'detail':'Invalid Password',
                    'status_code':status.HTTP_403_FORBIDDEN}
    else:
        return {'detail':'Invalid Email',
                'status_code':status.HTTP_401_UNAUTHORIZED}