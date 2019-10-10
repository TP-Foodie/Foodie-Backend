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
    GOOGLE_CLIENT_ID = os.getenv(
        "GOOGLE_CLIENT_ID",
        "218514362361-nchqu6j59rcskl1vmadfp6gl6ud8a0oo.apps.googleusercontent.com"
    )
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
