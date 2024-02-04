from pymongo import MongoClient

# Create a MongoDB client
client = MongoClient("mongodb+srv://anshvarshney20libra:ansh2012@cluster0.2ta0nkk.mongodb.net/?retryWrites=true&w=majority")
# client = MongoClient("mongodb://mongo:Fb31ABebaAhF32a66hc-D-AeEccd3bDG@monorail.proxy.rlwy.net:57476")

# client = MongoClient("mongodb://mongo:beD6AGD3b1Fdh-cEC253A5-EFBfa1d6g@monorail.proxy.rlwy.net:42951")
# Access the database and collection
db = client.Kriya_DB
# collection_name = db["todo_collection"]
investor_collection = db["investor_data"]
users_collection = db["users"]
creators_collection = db["creators_data"]
creators_payment_collection = db["creators_payment"]
