from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

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
class CreatorsPaymentSchema(BaseModel):
    creator_name: str = Field(...)
    gender: str = Field(...)
    upi: str = Field(...)
    bank_account_number: int = Field(...)
    ifsc: str = Field(...)
    account_holder_name: str = Field(...)
    phone_number: int = Field(...)

class PaymentDetailSchema(BaseModel):

    ticket_id:str=Field(...)
    creator_name:str = Field(...)
    phone_number:int=Field(...)
    amount:int=Field(...)
    transaction_mode:str=Field(...)
    transaction_date: Field(default_factory=datetime.utcnow)
    transaction_status:str=Field(...)
    class Config:
        arbitrary_types_allowed = True

class UserLoginSchema(BaseModel):
    email:EmailStr= Field(default=None)
    password:str = Field(default=None)
