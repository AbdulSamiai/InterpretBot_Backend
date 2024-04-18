from pydantic import BaseModel

class SignUp(BaseModel):
    UserName:str
    Email:str
    Password:str
    Location:str
    Language:int
    Discovered:str
    UserType:str
    Status:str

class LogIn(BaseModel):
    UserName:str
    Email:str
    Password:str
    
class ChangePassword(BaseModel):
    Email:str
    OldPassword:str
    NewPassword:str
    