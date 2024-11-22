from flask import Blueprint, request #jsonify converts python objects into JSON format
from services.property_services import PropertyServices
from services.http_responses import HttpResponse
from flask_cors import cross_origin
from services.cors_config import CORSConfig
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')
Local_uri = os.getenv("LOCAL_HOST")
http_responses = HttpResponse()
property_services = PropertyServices()

#Create a Blueprint
property_api_blueprint = Blueprint('properties', __name__)
#Initialize CORS on blueprint
cors_config = CORSConfig(origins=[Local_uri+"/api/properties"], headers=["Content-Type", "Authorization"])
cors_config.initialize_cors(property_api_blueprint)
class PropertyController:
    @cross_origin(supports_credentials=True)  
    @property_api_blueprint.route('/properties', methods=['GET']) #API endpoint
    def get_properties():
        try:
            selectedCity = request.args.get('selectedCity')
            propertyName = request.args.get('propertyName')
            filtered_properties = property_services.get_all(selectedCity, propertyName)
            return http_responses.successResponse(filtered_properties, 200)
            
        except Exception as error:
            return http_responses.errorResponse(str(error), 400)

        
    @cross_origin(supports_credentials=True)
    @property_api_blueprint.route('/properties/<id>', methods=['GET'])    
    def get_property(id):
        try:
            retrieved_property = property_services.get_property(id)
            return http_responses.successResponse(retrieved_property,200)
            
        except Exception as error:
            return http_responses.errorResponse(str(error),400)

    @cross_origin(supports_credentials=True)
    @property_api_blueprint.route('/properties', methods=['POST'])
    def insert_property():
        try:
            property_payload = request.get_json()
            inserted_property = property_services.insert_property(property_payload)
            return http_responses.successResponse(inserted_property, 201)
                        
        except Exception as error:
            return http_responses.errorResponse(str(error), 400)

    @cross_origin(supports_credentials=True)
    @property_api_blueprint.route('/properties/<id>', methods=['PUT'])
    def update_property(id):
        try:
            property_payload = request.get_json()
            updated_property = property_services.update_property(id, property_payload)
            return http_responses.successResponse(updated_property, 201)
        
        except Exception as error:
            return http_responses.errorResponse(str(error), 400)

    @cross_origin(supports_credentials=True)
    @property_api_blueprint.route('/properties/<id>', methods=['DELETE'])    
    def deactivate_property(id):
        try:
            deleted_property = property_services.deactivate_property(id)
            return http_responses.successResponse(deleted_property, 200)
        
        except Exception as error:
            return http_responses.errorResponse(str(error), 400)
        
    #This code provides a basic implementation of a Flask API endpoint for retrieving all properties from a MongoDB database. 
    #The jsonify function is used to create a JSON response that can be sent back to the client.
