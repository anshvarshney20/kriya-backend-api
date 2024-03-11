from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

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

class UserProfile(BaseModel):
    firstName: str
    lastName: str
    profileName: str
    phoneNumber: str
    email: str
    age: str
    gender: str
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    category: str
class UserRegisterSchema(BaseModel):
    fullname: str = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)


class CreatorsPaymentSchema(BaseModel):
    upi: str
    bank_account_number: int
    ifsc: str
    account_holder_name: str
    phone_number: int
    bank_name : str
    pancard_number : str
    adhaar_number : int
    # pancard_image:
    # adhaar_card_image:
    # passbook_image:int

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
    email:EmailStr= str
    password:str = str
