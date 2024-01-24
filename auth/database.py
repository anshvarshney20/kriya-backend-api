from pymongo import MongoClient

# Create a MongoDB client
client = MongoClient("mongodb+srv://anshvarshney20libra:ansh2012@cluster0.2ta0nkk.mongodb.net/?retryWrites=true&w=majority")
# client = MongoClient("mongodb://mongo:aeF-De3d2dE661Ghc44cF4GCgeDEafdH@viaduct.proxy.rlwy.net:40070")
# Access the database and collection
db = client.todo_db
# collection_name = db["todo_collection"]
investor_collection = db["investor_data"]
users_collection = db["users"]
