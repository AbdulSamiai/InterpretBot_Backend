from sqlalchemy.orm import Session
from app.routers.conversation import schemas
from app import models
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
from datetime import datetime

import whisper
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import soundfile as sf
import sounddevice as sd
from pathlib import Path



# Getting the model ready
load_dotenv('app/.env/keys.env')
OpenAIAPI_key = os.getenv('OpenAI_API_Key')
llm = ChatOpenAI(model = 'gpt-3.5-turbo' , temperature = 0 , openai_api_key=OpenAIAPI_key)
model = whisper.load_model("base")



def translateText(Text:str, TranslateTo:str):
    messages1 = [
        SystemMessage(
            content=f"You are a helpful assistant that can translate a user provided text to {TranslateTo} language."
        ),
        HumanMessage(
            content=Text
        ),
    ]
    response=llm(messages1)
    converted_text = response.content
    return converted_text



def checkLanguage(LangId:int,db:Session):
    lang = db.query(models.Language).\
        filter(models.Language.Id == LangId).first()
    return lang

def checkUser(UserId:int,db:Session):
    user = db.query(models.User).\
        filter(models.User.Id == UserId).first()
    return user

def conversation(data:schemas.CreateConversation,db: Session):
    conv = models.Conversation(UserId=data.UserId,
                               UserLanguage=data.UserLanguage,
                               TranslateTo=data.TranslateTo)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def conv_by_id(ConvId:int,db: Session):
    conv = db.query(models.Conversation).\
        filter(models.Conversation.Id == ConvId).first()
    return conv
 


# Saving user's audio file
def getfilepath(file):
    contents = file.file.read()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename_with_timestamp = f"{timestamp}_{file.filename}"    
    parent_dir='Static/Files'
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    file_path = f'{parent_dir}/{filename_with_timestamp}'
    with open(file_path, 'wb') as f:
            f.write(contents)
    return file_path


# Speech to text
def translation(translateTo:str,user_audio_file_path):
    transcribed_result = model.transcribe(audio=user_audio_file_path)
    messages2 = [
    SystemMessage(
        content=f"You are a helpful assistant that translates `{transcribed_result['language']}` text to `{translateTo}` language."
    ),
    HumanMessage(
      content=transcribed_result['text']
    ),
    ]
    response2 = llm(messages2)
    translated_text = response2.content

    return translated_text
    


# Translation and Saving output(Translated) file and returning the file
def interpretation(text):
    client = OpenAI(api_key= OpenAIAPI_key)
    parent_dir = 'Static/Files'
    response = client.audio.speech.create(
    model="tts-1-hd",
    voice="echo",
    input=text,
      speed=1.0
    )
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path = f"{parent_dir}/{timestamp}_Translated.wav" 
    response.stream_to_file(path)
    return path


# Playing output(Translated) audio
def play(filename):
        files_directory = Path('Static/Files')
        file_path = f"{files_directory}/{filename}"
        audio_data , sample_rate = sf.read(file=file_path)
        sd.play(data=audio_data,samplerate=sample_rate)
        sd.wait()