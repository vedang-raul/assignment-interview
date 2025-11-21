from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

from app.core.config import settings

load_dotenv()


# Add tlsCAFile=certifi.where() to the client connection to allow docker and mongo atlas to work together
client = MongoClient(settings.MONGO_URL, tlsCAFile=certifi.where())
db=client[settings.DB_NAME]

users_collection=db["users"]
tasks_collection=db["tasks"]

