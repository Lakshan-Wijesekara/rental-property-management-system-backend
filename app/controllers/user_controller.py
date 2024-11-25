from flask import Blueprint, request #jsonify converts python objects into JSON format
from services.user_services import UserServices
from services.http_responses import HttpResponse
from flask_cors import cross_origin
from services.cors_config import CORSConfig
from dotenv import load_dotenv
import os

#Get the Local URI
load_dotenv(dotenv_path='.env')
local_uri = os.getenv("LOCAL_HOST")
#Create the blueprint for users
user_api_blueprint = Blueprint('users', __name__)
#Initialize CORS on blueprint
cors_config = CORSConfig(origins=[local_uri+"/api/users"], headers=["Content-Type", "Authorization"])
cors_config.initialize_cors(user_api_blueprint)
http_response = HttpResponse()
user_services = UserServices()

class UserController:
    @cross_origin(supports_credentials=True)
    @user_api_blueprint.route('/users', methods=['GET'])
    def get_users():
        try:
            firstname = request.args.get('firstname')
            lastname = request.args.get('lastname')
            retrieved_users = user_services.get_all_users(firstname, lastname)
            return http_response.successResponse(retrieved_users, 200)
        except Exception as e:
            return http_response.errorResponse(str(e), 400)
        
    @cross_origin(supports_credentials=True)
    @user_api_blueprint.route('/users/<id>', methods=['GET'])
    def get_user(id):
        try:
            retrived_user = user_services.get_user(id)
            return http_response.successResponse(retrived_user,200)
        except Exception as e:
            return http_response.errorResponse(str(e),400)
    
    @cross_origin(supports_credentials=True)
    @user_api_blueprint.route('/users', methods=['POST'])
    def insert_user():
        try:
            user_payload = request.get_json()
            inserted_user = user_services.insert_user(user_payload)
            return http_response.successResponse(inserted_user,200)
        except Exception as e:
            return http_response.errorResponse(str(e),415)

    @cross_origin(supports_credentials=True)    
    @user_api_blueprint.route('/users/<id>', methods=['PUT'])
    def update_user(id):
        try:
            user_payload = request.get_json()
            updated_user = user_services.update_user(id,user_payload)
            return http_response.successResponse(updated_user,200)
        except Exception as e:
            return http_response.errorResponse(str(e),415)
    
    @cross_origin(supports_credentials=True)    
    @user_api_blueprint.route('/users/<id>', methods=['DELETE'])
    def delete_user(id):
        try:
            deleted_user = user_services.deactivate_user(id)
            return http_response.successResponse(deleted_user,200)
        except Exception as e:
            return http_response.errorResponse(str(e),404)
        

