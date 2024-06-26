from datetime import datetime
from fastapi import FastAPI, Body, HTTPException, Depends, Query,Form,File,UploadFile,status
from auth.models import UserRegisterSchema, UserLoginSchema, InvestorSchema,CreatorsPaymentSchema,PaymentDetailSchema
from auth.jwt_handler import signJWT
from auth.database import users_collection, investor_collection, creators_collection,creators_payment_collection,creators_signup_collection
from passlib.context import CryptContext
from typing import List
from enum import Enum
from auth.security import hash_password
from auth.jwt_bearer import JWTBearer
from pydantic import ValidationError,BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Routes.Routes import router

app = FastAPI()
app.include_router(router)
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5173",
    "https://kriya-test-env.web.app",
    "https://creatorsapp.in"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8080)

# from fastapi import FastAPI
# from pymongo import MongoClient
#
# app = FastAPI()
#
# # Connect to MongoDB
# client = MongoClient("mongodb+srv://doadmin:kGnA514V3762l9Wr@db-mongodb-nyc3-27233-c025f978.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc3-27233")
# db = client["Kriya_DB"]
# collection = db["users"]
#
# @app.get("/")
# async def read_root():
#     # Fetch some data from MongoDB
#     data = collection.find_one()
#
#     return {"message": "MongoDB connected successfully", "data": data}
