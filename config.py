import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI")
    
    # JWT Configuration
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "60"))
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Validate critical environment variables
    @classmethod
    def validate_config(cls):
        missing_vars = []
        if not cls.MONGO_URI:
            missing_vars.append("MONGO_URI")
        if not cls.JWT_SECRET:
            missing_vars.append("JWT_SECRET")
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def __init__(self):
        self.validate_config()
