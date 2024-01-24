from pydantic import BaseModel, Field, EmailStr


class InvestorSchema(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    age: int = Field(...)
    profile_name: str = Field(...)
    gender:str = Field(...)
    about_me:str = Field(...)
    per_chat_price:int = Field(...)
    call_per_price:int = Field(...)
    email:str = Field(...)
    phonenumber:int = Field(...)



class UserRegisterSchema(BaseModel):
    fullname: str = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)
    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any"
            }
        }

class UserLoginSchema(BaseModel):
    email:EmailStr= Field(default=None)
    password:str = Field(default=None)
