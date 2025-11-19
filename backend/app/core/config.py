import os
from dotenv import load_dotenv

# Load the .env file once, here
load_dotenv()

class Settings:
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "intern_assignment")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ADMIN_CODE: str = os.getenv("ADMIN_CODE", "YouKnowNothingJonSnow")

settings = Settings()
