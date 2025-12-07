from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()


MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'mano_mitra')


_client = None


def get_db():
global _client
if _client is None:
_client = MongoClient(MONGO_URI)
return _client[DB_NAME]




def save_session(db, user_id, payload):
db.sessions.insert_one({'user_id': user_id, 'payload': payload})




def get_user(db, user_id):
return db.users.find_one({'user_id': user_id})




def create_user(db, profile):
db.users.insert_one(profile)