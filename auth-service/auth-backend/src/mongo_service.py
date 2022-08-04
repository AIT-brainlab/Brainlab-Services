from enum import unique
from pymongo import MongoClient
from pymongo.collection import Collection
from config import DB_NAME, USER_COLLECTION_NAME, FORGOT_PASSWORD_TOKEN_COLLECTION_NAME, USER_SESSION_COLLECTION_NAME

class MongoService():
    instance:MongoClient | None = None

    @staticmethod
    def get_instance()->MongoClient:
        if MongoService.instance is None:
            username:str
            password:str
            with open('/run/secrets/all_db_user.txt','r') as u_file:
                username = u_file.read()
            with open('/run/secrets/all_db_password.txt','r') as p_file:
                password = p_file.read()
            MongoService.instance = MongoClient(f'mongodb://{username}:{password}@coredb:27017')
        return MongoService.instance

    @staticmethod
    def get_user_collection_instance()->Collection:
        return MongoService.get_instance()[DB_NAME][USER_COLLECTION_NAME]

    @staticmethod
    def get_forget_password_token_instance()->Collection:
        return MongoService.get_instance()[DB_NAME][FORGOT_PASSWORD_TOKEN_COLLECTION_NAME]
    
    @staticmethod
    def get_user_session_instance()->Collection:
        return MongoService.get_instance()[DB_NAME][USER_SESSION_COLLECTION_NAME]
    @staticmethod 
    def init_db()->None:
        MongoService.get_user_collection_instance().create_index("username",unique=True)
        MongoService.get_user_collection_instance().create_index("user_id",unique=True)
 
        MongoService.get_forget_password_token_instance().create_index("token",unique=True)
        MongoService.get_forget_password_token_instance().create_index("created_time",expireAfterSeconds= 5*60 )

        MongoService.get_user_session_instance().create_index("session_id",unique=True)
        MongoService.get_user_session_instance().create_index("created_time",expireAfterSeconds = 7*24*60)
