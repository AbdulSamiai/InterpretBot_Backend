from fastapi import APIRouter,Depends,HTTPException,status

from sqlalchemy.orm import Session
from app.routers.language import schemas,crud

from app.database import get_db


router = APIRouter(
    tags=['Language'],
    prefix='/Language'
)

@router.post('/Enter-Language')
async def enterlanguage(data:schemas.EnterLanguage,db:Session = Depends(get_db)):
    
    lang_check = crud.get_language_by_name(LanguageName=data.LanguageName,db=db)
    if lang_check:
        return {'detail':'Language already added',
                'status_code':status.HTTP_406_NOT_ACCEPTABLE}
    else:
        newLang = crud.add_language(data=data,db=db)
        return {'detail':{
            'LanguageId':newLang.Id,
            'Language':newLang.LanguageName
        },
            'status_code':status.HTTP_200_OK}

@router.get('/Show-All-Languages')
def showlanguage(db: Session = Depends(get_db)):
    languages = crud.show_Languages(db=db)
    if languages:
        return {'detail':{
            'AllLanguages': languages
        },
            'status_code':status.HTTP_200_OK}
    else:
        return {'detail':'No Languages found',
                'status_code':status.HTTP_404_NOT_FOUND}