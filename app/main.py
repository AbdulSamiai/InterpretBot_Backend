from fastapi import FastAPI
from routers.user import user
from routers.conversation import conversation
from routers.language import language
from models import Base
from database import engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# Base.metadata.create_all(engine)


app = FastAPI()
app.include_router(user.router)
app.include_router(conversation.router)
app.include_router(language.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__=='__main__':
    uvicorn.run(app=app,host='192.168.18.84',port=11000)
