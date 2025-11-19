from pymongo import MongoClient
import os
from dotenv import load_dotenv

from app.core.config import settings

load_dotenv()



client=MongoClient(settings.MONGO_URL)
db=client[settings.DB_NAME]

users_collection=db["users"]
tasks_collection=db["tasks"]

