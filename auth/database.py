from pymongo import MongoClient

# Create a MongoDB client
# client = MongoClient("mongodb+srv://anshvarshney20libra:ansh2012@cluster0.2ta0nkk.mongodb.net/?retryWrites=true&w=majority")
# mongodb://mongo:beD6AGD3b1Fdh-cEC253A5-EFBfa1d6g@monorail.proxy.rlwy.net:42951
# client = MongoClient("mongodb://mongo:beD6AGD3b1Fdh-cEC253A5-EFBfa1d6g@monorail.proxy.rlwy.net:42951")
client = MongoClient("mongodb+srv://doadmin:kGnA514V3762l9Wr@db-mongodb-nyc3-27233-c025f978.mongo.ondigitalocean.com/Kriya_DB?tls=true&authSource=admin&replicaSet=db-mongodb-nyc3-27233")

# Access the database and collection
db = client.Kriya_DB
# collection_name = db["todo_collection"]
investor_collection = db["investor_data"]
users_collection = db["users"]
creators_collection = db["creators_data"]
creators_payment_collection = db["creators_payment"]
creators_signup_collection = db["creators_signup"]
