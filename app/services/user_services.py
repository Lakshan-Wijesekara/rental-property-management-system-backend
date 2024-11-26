from flask import jsonify
from services.db_connection import MongoDBConnection, user_collection_name
from services.http_responses import HttpResponse
from services.util_services import UtilService
from models.user_model import User
class UserServices:
    def __init__(self):
        db_connection = MongoDBConnection()
        self.utility_services = UtilService()
        self.http_response = HttpResponse()
        self.user_collection = db_connection.get_userCollection(user_collection_name)

    def get_all_users(self, firstname, lastname):
        try:
            #Filter using query parameters
            user_filter_query = {}
            if firstname:
                user_filter_query["firstname"] = {"$regex": f"^{firstname}", "$options": "i"}
            if lastname:
                user_filter_query["lastname"] = {"$regex": f"^{lastname}", "$options": "i"}
            user_filter_query['is_active'] = True
            users = self.user_collection.find(user_filter_query)
            users_objects = self.utility_services.convert_cursor_object(users)
            if users_objects:
                return users_objects
            else:
                return "No record found!" 
        except:
            raise

    def get_user(self,id):
        try:
            user_id = self.utility_services.convert_object_id(id)
            retrieved_user = self.user_collection.find_one({'_id': user_id})
            retrieved_user_doc = self.utility_services.convert_cursor_object(retrieved_user)
            if retrieved_user_doc:
                return retrieved_user_doc
            else:
                return ValueError("No record found from the given ID!")
        except:
            raise

    def insert_user(self, user_payload):
        try:
            if isinstance(user_payload, User):
                user_instance = User(**user_payload)
                user_instance_dict = user_instance.__dict__.copy()
                inserted_user_id = self.user_collection.insert_one(user_instance_dict).inserted_id
                return str(inserted_user_id)
            else:
                raise ValueError      
        except:
            raise

    def update_user(self, id, user_payload):
        try:
            user_instance = User(**user_payload)
            if isinstance(user_instance, User):
                user_instance_dict = user_instance.__dict__.copy()
                user_id = self.utility_services.convert_object_id(id)
                updated_user_record = self.user_collection.update_one({'_id': user_id}, {"$set":user_instance_dict} )
                updated_user_count = updated_user_record.modified_count
                if updated_user_count>0:
                    return str(user_id)
                else:
                    return "This user has been already updated with the given data!"
            else:
                raise ValueError
        except:
            raise

    def deactivate_user(self, id):
        try:            
            document_id = self.utility_services.convert_object_id(id)
            deactivated_user = self.user_collection.update_one({"_id":document_id}, {"$set":{"is_active": False}})
            if deactivated_user.modified_count>0:
                return str(document_id)
            else:
                return "No user found to delete or the requested user already has been deleted!"
        except:
            raise