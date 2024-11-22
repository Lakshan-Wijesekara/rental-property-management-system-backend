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
            retrived_property = user_services.get_user(id)
            return http_response.successResponse(retrived_property,200)
        except Exception as e:
            return http_response.errorResponse(str(e),400)
