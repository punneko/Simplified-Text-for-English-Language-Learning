from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client.simplifyme_db
users_collection = db.users
history_collection = db.history

# unique indexes
users_collection.create_index("email", unique=True)
users_collection.create_index("google_id", unique=True, sparse=True)
users_collection.create_index("name", unique=True, sparse=True)

history_collection.create_index("user_id")
history_collection.create_index([("user_id", 1), ("created_at", -1)])
