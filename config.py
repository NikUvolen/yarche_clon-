import os
from dotenv import load_dotenv


load_dotenv()

API_ID = int(os.getenv('api_id'))
API_HASH = os.getenv('api_hash')
SESSION_STRING = os.getenv('session_string')
BOT_ID = os.getenv('bot_id')
