from pydantic import BaseModel

class Conversation(BaseModel):
    UserLanguage:int
    TranslateTo:int
    