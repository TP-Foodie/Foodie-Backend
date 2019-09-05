from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(verbose=True)

env_path = '/.env'
load_dotenv(dotenv_path=env_path)


class Config:
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "27017")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "app")
    DATABASE_AUTH_SOURCE = os.getenv("DATABASE_AUTH_SOURCE", "foodie")
    DATABASE_AUTH_MECHANISM = os.getenv("DATABASE_AUTH_MECHANISM", "SCRAM-SHA-1")
