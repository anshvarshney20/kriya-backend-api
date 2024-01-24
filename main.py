from fastapi import FastAPI, Body, HTTPException, Depends, Query,Form,File,UploadFile
from auth.models import UserRegisterSchema, UserLoginSchema, InvestorSchema
from auth.jwt_handler import signJWT
from auth.database import users_collection, investor_collection
from passlib.context import CryptContext
from typing import List
from auth.security import hash_password
from auth.jwt_bearer import JWTBearer
from fastapi.responses import JSONResponse

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def user_exists(email: str):
    return users_collection.find_one({"email": email}) is not None


@app.post("/create/investors", dependencies=[Depends(JWTBearer())], tags=["investor"])
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
    profile_image: UploadFile = File(...),
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

@app.get(
    "/investors",
    dependencies=[Depends(JWTBearer())],
    response_model=List[InvestorSchema],
)
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


@app.post("/user/signup", tags=["user"])
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


@app.post("/user/login", tags=["user"])
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
