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
            if len(users_objects)>0:
                return users_objects
            else:
                return "No record found!" 
        except:
            raise

    def get_user(self,id):
        try:
            user_id = self.utility_services.convert_object_id(id)
            retrieved_user = self.user_collection.find({'_id': user_id})
            retrieved_user_property = self.utility_services.convert_cursor_object(retrieved_user)
            if retrieved_user_property==[]:
                raise ValueError("No record found from the given ID")
            else:
                return retrieved_user_property
        except:
            raise
