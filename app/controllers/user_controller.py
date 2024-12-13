from flask import Blueprint, make_response, request #jsonify converts python objects into JSON format
from services.user_services import UserServices
from services.http_responses import HttpResponse
from flask_cors import cross_origin
from services.cors_config import CORSConfig
from dotenv import load_dotenv
from services.exceptions import CustomExceptions
from services.auth_guard import auth_required
import os

#Get the Local URI
load_dotenv(dotenv_path='.env')
local_uri = os.getenv("LOCAL_HOST")
#Create the blueprint for users
user_api_blueprint = Blueprint('users', __name__)
#Initialize CORS on blueprint
cors_config = CORSConfig(origins=[os.getenv("FRONT_END_URI")], headers=["Content-Type", "Authorization"], supports_credentials=True)
cors_config.initialize_cors(user_api_blueprint)
http_response = HttpResponse()
user_services = UserServices()
custom_exceptions = CustomExceptions()

class UserController:
    @cross_origin(supports_credentials=True)
    @user_api_blueprint.route('/users', methods=['GET', 'OPTIONS'])
    @auth_required
    def get_users():
        if request.method == 'OPTIONS':
    # Respond to preflight request
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
            response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")

            return response, 204
        try:
            firstname = request.args.get('firstname')
            lastname = request.args.get('lastname')
            retrieved_users = user_services.get_all_users(firstname, lastname)
            
            return http_response.successResponse(retrieved_users, 200)

        except Exception as e:

            return custom_exceptions.app_exceptions(e)
        
    @cross_origin(supports_credentials=True)
    @user_api_blueprint.route('/users/<id>', methods=['GET'])
    @auth_required
    def get_user(id):
        try:
            retrived_user = user_services.get_user(id)
            return http_response.successResponse(retrived_user, 200)

        except Exception as e:

            return custom_exceptions.app_exceptions(e)
    
    @cross_origin(supports_credentials=True)
    @user_api_blueprint.route('/login', methods=['POST', 'OPTIONS'])
    def auth_user():
        if request.method == 'OPTIONS':
        # Respond to preflight request
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            
            return response, 204
        try:
            data_received = request.json
            username_received = data_received.get('username')
            password_received = data_received.get('password')
            user_token = user_services.authenticate(username_received, password_received)
            
            if user_token:
                return http_response.successResponse(user_token, 200)
            else:
                return http_response.errorResponse("No user token found!", 401)
        except Exception as e:

            return custom_exceptions.app_exceptions(e)
   
    @cross_origin(supports_credentials=True)
    @user_api_blueprint.route('/users', methods=['POST'])
    @auth_required
    def insert_user():
        try:
            user_payload = request.get_json()
            user_payload['is_active'] = True
            inserted_user = user_services.insert_user(user_payload)

            return http_response.successResponse(inserted_user, 200)

        except Exception as e:

            return custom_exceptions.app_exceptions(e)

    @cross_origin(supports_credentials=True)    
    @user_api_blueprint.route('/users/<id>', methods=['OPTIONS', 'PUT'])
    @auth_required
    def update_user(id):
        try:
            user_payload = request.get_json()
            user_payload['is_active'] = True
            updated_user = user_services.update_user(id, user_payload)
            return http_response.successResponse(updated_user, 200)

        except Exception as e:

            return custom_exceptions.app_exceptions(e)
        
    @cross_origin(supports_credentials=True)    
    @user_api_blueprint.route('/users/<id>', methods=['DELETE'])
    @auth_required
    def delete_user(id):
        try:
            deleted_user = user_services.deactivate_user(id)
            return http_response.successResponse(deleted_user, 200)

        except Exception as e:

            return custom_exceptions.app_exceptions(e)