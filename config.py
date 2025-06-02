import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv('DATABASE_URL')

class Config:
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
