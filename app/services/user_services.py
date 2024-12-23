from services.db_connection import MongoDBConnection, user_collection_name
from services.http_responses import HttpResponse
from services.util_services import UtilService
from models.user_model import User
from services.exceptions import InvalidResponse
from services.jwt_handler import generate_jwt
from services.authentication import AuthenticationService

class UserServices:
    def __init__(self):
        db_connection = MongoDBConnection()
        self.utility_services = UtilService()
        self.http_response = HttpResponse()
        self.user_authentication = AuthenticationService()
        self.user_collection = db_connection.get_userCollection(user_collection_name)

    def authenticate(self, username, password):
        try:
            user_collection =  self.user_collection
            user_data = user_collection.find_one({"username": username})
            user_json = self.utility_services.convert_cursor_object(user_data)
            database_pwd = user_data.get("password")
            if user_data != None:
                check_pwd = self.user_authentication.authenticate_user(password, database_pwd)
                if check_pwd == True:
                    token = generate_jwt(payload=user_json, lifetime=1)

                    return token
                else:
                    raise InvalidResponse("Invalid Username or Password!", 401)
                
        except:
            raise

    def get_all_users(self, firstname, lastname):
        try:
            #Filter using query parameters
            user_filter_query = {"is_active": True}
            if firstname:
                user_filter_query["firstname"] = {"$regex": f"^{firstname}", "$options": "i"}
            if lastname:
                user_filter_query["lastname"] = {"$regex": f"^{lastname}", "$options": "i"}
            users = self.user_collection.find(user_filter_query)
            users_objects = self.utility_services.convert_cursor_object(users)
            if users_objects:
                return users_objects
            else:
                raise InvalidResponse("No records were found!", 400)

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
                raise InvalidResponse("No user found from the given ID!", 400)

        except:
            raise

    def insert_user(self, user_payload):
        try:
            #Used the pydantic to validate the user_instance. It goes to except when failed the validation
            user_payload['is_active'] = True
            user_instance = User(**user_payload)
            if user_instance:
                user_instance_dict = user_instance.__dict__.copy()
                inserted_user_id = self.user_collection.insert_one(user_instance_dict).inserted_id

                return str(inserted_user_id)

        except:
            raise InvalidResponse("No user record was created, please check all required user parameters!", 400)

    def update_user(self, id, user_payload):
        try:
            user_payload['is_active'] = True
            user_instance = User(**user_payload)
            user_instance_dict = user_instance.__dict__.copy()
            user_id = self.utility_services.convert_object_id(id)
            update_filter = {'_id': user_id}
            update_operation = {"$set":user_instance_dict}
            updated_user_record = self.user_collection.update_one(update_filter, update_operation).modified_count
            if updated_user_record>0:
                return str(user_id)
            else:
                raise InvalidResponse("No records were modified!", 400)

        except:
            raise InvalidResponse("Operation failed, please check all required user parameters!", 400)

    def deactivate_user(self, id):
        try:            
            document_id = self.utility_services.convert_object_id(id)
            deactivate_filter = {"_id":document_id}, 
            deactivate_operation = {"$set":{"is_active": False}}
            deactivated_user = self.user_collection.update_one(deactivate_filter, deactivate_operation).modified_count
            if deactivated_user>0:
                return str(document_id)
            else:
                raise InvalidResponse("No matching record found to delete!", 400)

        except:
            raise