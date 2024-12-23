from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client["rag_chat_db"]
        self.messages = self.db["messages"]
        self.files = self.db["files"]

    def save_message(self, user, message, timestamp):
        return self.messages.insert_one({
            "user": user,
            "message": message,
            "timestamp": timestamp
        })

    def get_messages(self, limit=50):
        return list(self.messages.find().sort("timestamp", -1).limit(limit))

    def save_file(self, filename, file_data, user):
        return self.files.insert_one({
            "filename": filename,
            "data": file_data,
            "user": user
        })

    def get_file(self, filename):
        return self.files.find_one({"filename": filename})