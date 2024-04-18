from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.conversation import schemas,crud
from fastapi import File,UploadFile
import os
from fastapi.responses import FileResponse




router = APIRouter(
    tags=['Conversation'],
    prefix='/Conversation'
)


@router.post('/Create-Conversation')
async def userlanguage(data:schemas.CreateConversation,db: Session=Depends(get_db)):
    try:
        user = crud.checkUser(UserId=data.UserId,db=db)
        if user:
            userlang = crud.checkLanguage(LangId=data.UserLanguage,db=db)
            if userlang:
                translatelang = crud.checkLanguage(LangId=data.TranslateTo,db=db)
                if translatelang:
                    conv = crud.conversation(data=data,db=db)
                    if conv:
                        return {'detail':{
                            'Message':'Conversation created successfully',
                            'ConversationId':conv.Id
                        },
                            'status_code':status.HTTP_200_OK}
                    else:
                        return {'detail':'Translating Language does not exist',
                                'status_code':status.HTTP_404_NOT_FOUND}
            else:
                return {'detail':'User Language does not exist',
                        'status_code':status.HTTP_404_NOT_FOUND}
        else:
            return {'detail':'User does not exist',
                    'status_code':status.HTTP_404_NOT_FOUND}
    except:
        return HTTPException(detail='Something went wrong',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@router.get('/Get-Conv-By-Id')
def get_conv_by_id(ConvId: int,db: Session=Depends(get_db)):
    conv = crud.conv_by_id(ConvId=ConvId,db=db)
    user = crud.checkUser(UserId=conv.UserId,db=db)
    userlang = crud.checkLanguage(LangId=conv.UserLanguage,db=db)
    translatelang = crud.checkLanguage(LangId=conv.TranslateTo,db=db)
    
    if conv:
        return {'detail':{
            'UserId':user.Id,
            'UserLanguage':userlang.LanguageName,
            'TranslateTo':translatelang.LanguageName
        },
                'status_code':status.HTTP_200_OK}
    else:
        return HTTPException(detail='Conversation Not Found',status_code=status.HTTP_404_NOT_FOUND)


@router.post('/Basic-Language-Translation')
async def basicLanguageTranslation(Text:str,TranslateTo:str):
    try:
        TranslatedText = crud.translateText(Text=Text,TranslateTo=TranslateTo)
        return {'detail':{
            'TranslatedText':TranslatedText
        },
                'status_code':status.HTTP_200_OK}
    except:
        return HTTPException(detail='Something went wrong',status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post('/Interpretation')
async def interpret(translateTo:str,file:UploadFile=File(...)):
    try:
        file_path = crud.getfilepath(file=file)
        absoluteFilePath = os.path.abspath(file_path)
        translated_text = crud.translation(translateTo=translateTo,user_audio_file_path=absoluteFilePath)
        path = crud.interpretation(text=translated_text)
        return path
    except:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail='Something went wrong')


@router.get("/audio/{file_path:path}")
async def get_audio_file(file_path: str):
    media_type = "audio/wave"
    return FileResponse(path=file_path, media_type=media_type)


@router.get('/Play/{filename}')
def play_audio(filename:str):
    return crud.play(filename=filename)