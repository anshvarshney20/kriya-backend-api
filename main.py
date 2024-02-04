from datetime import datetime
from fastapi import FastAPI, Body, HTTPException, Depends, Query,Form,File,UploadFile,status
from auth.models import UserRegisterSchema, UserLoginSchema, InvestorSchema,CreatorsPaymentSchema,PaymentDetailSchema
from auth.jwt_handler import signJWT
from auth.database import users_collection, investor_collection, creators_collection,creators_payment_collection
from passlib.context import CryptContext
from typing import List
from enum import Enum
from auth.security import hash_password
from auth.jwt_bearer import JWTBearer
from pydantic import ValidationError,BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class ValidationErrorResponse(BaseModel):
    detail: List[dict]

class TransactionMode(str, Enum):
    credit = "UPI"
    debit = "Bank Transfer"

class TransactionStatus(str, Enum):
    success = "Success"
    pending = "Pending"
    failed = "Failed"

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def user_exists(email: str):
    return users_collection.find_one({"email": email}) is not None


@app.post("/create/investors", dependencies=[Depends(JWTBearer())], tags=["POST Data"])
def post_investor(
    first_name: str = Form(...),
    last_name: str = Form(...),
    age: int = Form(...),
    profile_name: str = Form(...),
    gender: str = Form(...),
    about_me: str = Form(...),
    per_chat_price: float = Form(...),
    call_per_price: float = Form(...),
    email: str = Form(...),
    phonenumber: str = Form(...),
    token: str = Depends(JWTBearer()),
):
    investor_data = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "profile_name": profile_name,
        "gender": gender,
        "about_me": about_me,
        "per_chat_price": per_chat_price,
        "call_per_price": call_per_price,
        "email": email,
        "phonenumber": phonenumber,

    }
    # Your logic for storing investor_data in the database goes here
    investor_collection.insert_one(investor_data)

    return {"message": "Investor created successfully"}

@app.post('/creators/details',dependencies=[Depends(JWTBearer())], tags=["POST Data"])
def post_creator(
    creator_name: str = Form(...),
    gender: str = Form(...),
    upi: str = Form(...),
    bank_account_number: int = Form(...),
    ifsc: str = Form(...),
    account_holder_name: str = Form(...),
    phone_number: int = Form(...),
    token: str = Depends(JWTBearer()),
):
    creator_data = CreatorsPaymentSchema(
        creator_name=creator_name,
        gender=gender,
        upi=upi,
        bank_account_number=bank_account_number,
        ifsc=ifsc,
        account_holder_name=account_holder_name,
        phone_number=phone_number
    )
    creators_collection.insert_one(dict(creator_data))
    return {"message":"Creators Details Created Successfully"}

@app.get("/creators",dependencies=[Depends(JWTBearer())], tags=['GET Data'])
def get_creators(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000),token: str = Depends(JWTBearer()),):
    creators = list(creators_collection.find().skip(skip).limit(limit))
    valid_creators = [
        inv
        for inv in creators
        if all(key in inv for key in CreatorsPaymentSchema.__annotations__.keys())
    ]

    creators_schema: List[CreatorsPaymentSchema] = []

    try:
        creators_schema = [CreatorsPaymentSchema(**creator) for creator in valid_creators]
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": e.errors(), "message": "Validation Error"}
        )

    return creators_schema

@app.post("/payment-details",dependencies=[Depends(JWTBearer())], tags=['Payment Module'])
def payment_details(
    ticket_id: str = Form(...),
    creator_name: str = Form(...),
    amount: int = Form(...),
    phone_number:int = Form(...),
    transaction_mode: TransactionMode = Form(...),
    transaction_status: TransactionStatus = Form(...),
    token: str = Depends(JWTBearer()),
):
    # Check if a document with the same ticket_id already exists
    existing_payment = creators_payment_collection.find_one({"ticket_id": ticket_id})
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": f"Payment with ticket_id '{ticket_id}' already exists"}
        )

    transaction_date = datetime.now()
    try:
        # Parse the transaction_date string to a datetime object
        transaction_date = datetime.now()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Invalid transaction_date format"}
        )

    payment_data = PaymentDetailSchema(
        ticket_id=ticket_id,
        creator_name=creator_name,
        amount=amount,
        phone_number=phone_number,
        transaction_mode=transaction_mode.value,
        transaction_date=transaction_date,
        transaction_status=transaction_status.value,
    )

    # Your logic for handling payment_data goes here
    creators_payment_collection.insert_one(dict(payment_data))
    return {"message": "Payment details created successfully"}
@app.get("/payment-details", dependencies=[Depends(JWTBearer())],tags=['Payment Module'])
def get_creators_payment(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000),token: str = Depends(JWTBearer()),):
    creators_payment = list(creators_payment_collection.find().skip(skip).limit(limit))
    valid_creators = [
        inv
        for inv in creators_payment
        if all(key in inv for key in PaymentDetailSchema .__annotations__.keys())
    ]
    try:
        creators_schema = [PaymentDetailSchema(**creator) for creator in valid_creators]
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": e.errors(), "message": "Validation Error"}
        )

    return creators_schema

@app.get("/creators-payment/search", dependencies=[Depends(JWTBearer())],tags=['Search Creators Payment'])
def search_creators_payment(
    ticket_id: str = Query(..., title="Ticket ID", description="Enter the ticket ID to search"),
    token: str = Depends(JWTBearer()),
):
    # Perform the search based on the provided ticket_id
    creators_payment = list(creators_payment_collection.find({"ticket_id": ticket_id}))

    valid_creators = [
        inv
        for inv in creators_payment
        if all(key in inv for key in PaymentDetailSchema.__annotations__.keys())
    ]

    try:
        creators_schema = [PaymentDetailSchema(**creator) for creator in valid_creators]
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": e.errors(), "message": "Validation Error"}
        )

    return creators_schema

@app.get('/all-creators-payment-search', dependencies=[Depends(JWTBearer())],tags=['Search Creators Payment'])
def all_creators_payment_search(
     creator_name: str = Query(None, title="Creator Name", description="Enter the Creator Name to search"),
     phone_number: int = Query(None, title="Phone Number", description="Enter the Phone Number to search"),
     token: str = Depends(JWTBearer()),
):
    # Define a filter based on the provided parameters
    filter_params = {}
    if creator_name:
        filter_params["creator_name"] = creator_name
    if phone_number:
        filter_params["phone_number"] = phone_number

    # Fetch documents based on the filter
    creators_payment = list(creators_payment_collection.find(filter_params))

    # Validate and convert to Pydantic schema
    valid_creators = [
        inv
        for inv in creators_payment
        if all(key in inv for key in PaymentDetailSchema.__annotations__.keys())
    ]
    try:
        creators_schema = [PaymentDetailSchema(**creator) for creator in valid_creators]
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": e.errors(), "message": "Validation Error"}
        )

    return creators_schema
@app.get("/investors",dependencies=[Depends(JWTBearer())],response_model=List[InvestorSchema],tags=['GET Data'])
def get_investors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    token: str = Depends(JWTBearer()),
):
    investors = list(investor_collection.find().skip(skip).limit(limit))

    valid_investors = [
        inv
        for inv in investors
        if all(key in inv for key in InvestorSchema.__annotations__.keys())
    ]

    investors_schema = [InvestorSchema(**inv) for inv in valid_investors]

    return investors_schema


@app.post("/user/signup", tags=["Admin Authentication"])
def create_user(
    fullname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    if user_exists(email):
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    hashed_password = hash_password(password)

    user_data = {
        "fullname": fullname,
        "email": email,
        "hashed_password": hashed_password,
    }

    users_collection.insert_one(user_data)

    jwt_token = signJWT(email)
    return JSONResponse(
        content={"message": "User created successfully", "token": jwt_token}
    )


@app.post("/user/login", tags=["Admin Authentication"])
def user_login(
    email: str = Form(...),
    password: str = Form(...),
):
    user_data = users_collection.find_one({"email": email})

    if user_data and verify_password(password, user_data["hashed_password"]):
        return signJWT(email)
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
