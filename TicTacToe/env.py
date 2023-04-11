import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_DATABASE')

ADMINS = os.getenv('ADMINS').split()
