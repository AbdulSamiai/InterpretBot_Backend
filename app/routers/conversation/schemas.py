from pydantic import BaseModel

class CreateConversation(BaseModel):
    UserId:int
    UserLanguage:int
    TranslateTo:int