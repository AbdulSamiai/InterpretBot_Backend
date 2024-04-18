from sqlalchemy.orm import Session
from app import models
from app.routers.language import schemas

def get_language_by_name(LanguageName:str,db:Session):
    lang = db.query(models.Language).filter(models.Language.LanguageName == LanguageName).first()
    return lang

def add_language(data:schemas.EnterLanguage,db: Session):
    newLanguage = models.Language(LanguageName=data.LanguageName)
    db.add(newLanguage)
    db.commit()
    db.refresh(newLanguage)
    return newLanguage

def show_Languages(db: Session):
    languages = db.query(models.Language).all()
    return languages