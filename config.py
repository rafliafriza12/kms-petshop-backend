import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "60"))
