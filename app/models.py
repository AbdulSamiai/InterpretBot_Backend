from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = 'User'
    
    
    Id = Column(Integer,primary_key=True)
    UserName = Column(String)
    Email = Column(String,unique=True)
    Password = Column(String)
    Location = Column(String)
    Language = Column(Integer)
    Discovered = Column(String)
    UserType = Column(String)
    Status = Column(String)
    
    Conversation = relationship('Conversation',back_populates='User')



class Language(Base):
    __tablename__ = 'Language'
    
    Id = Column(Integer,primary_key=True)
    LanguageName = Column(String,unique=True)
    
    
    
class Conversation(Base):
    __tablename__ = 'Conversation'
    
    Id = Column(Integer,primary_key=True)
    UserId = Column(Integer,ForeignKey('User.Id'))
    UserLanguage = Column(Integer)
    TranslateTo = Column(Integer)
    
    User = relationship('User',back_populates='Conversation')
    ChatHistory = relationship('ChatHistory',back_populates='Conversation')
    
    
    
class ChatHistory(Base):
    __tablename__ = 'ChatHistory'
    
    
    Id = Column(Integer,primary_key=True)
    ConversationId = Column(Integer,ForeignKey('Conversation.Id'))
    AudioFilePath = Column(String)
    Chat = Column(String)
    
    Conversation = relationship('Conversation',back_populates='ChatHistory')