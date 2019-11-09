import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

ENV_PATH = '/.env'
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    DATABASE_NAME = os.getenv("DATABASE_NAME", "foodie")
    DATABASE_SSL = os.getenv("DATABASE_SSL", "false").lower() == "true"
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = int(os.getenv("DATABASE_PORT", "27017"))
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "app")
    DATABASE_AUTH_SOURCE = os.getenv("DATABASE_AUTH_SOURCE", "foodie")
    JWT_SECRET = os.getenv("JWT_SECRET", "foodie")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./src/google_credentials.json")
    MAP_QUEST_API_KEY = os.getenv("MAP_QUEST_API_KEY", "")
