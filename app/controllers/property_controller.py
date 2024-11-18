from flask import Blueprint, jsonify, request #jsonify converts python objects into JSON format
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
api_blueprint = Blueprint('properties_api', __name__)
#Initialize CORS on blueprint
cors_config = CORSConfig(origins=[Local_uri+"/api/properties"], headers=["Content-Type", "Authorization"])
cors_config.initialize_cors(api_blueprint)
class PropertyController:
    @cross_origin(supports_credentials=True)  
    @api_blueprint.route('/properties', methods=['GET']) #API endpoint
    def get_properties():
        try:
            selectedCity = request.args.get('selectedCity')
            propertyName = request.args.get('propertyName')
            filtered_properties = property_services.get_all(selectedCity, propertyName)
            return http_responses.successResponse(filtered_properties)
            
        except Exception as error:
            error_at_exception = http_responses.errorResponse(str(error))
            return error_at_exception
        
    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['GET'])    
    def get_property(id):
        try:
            retrieved_property = property_services.get_property(id)
            if retrieved_property == None:
                raise ValueError("Property id not found!")
            else:
                return http_responses.successResponse(retrieved_property)
            
        except Exception as error:
            return http_responses.errorResponse(str(error))

    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties', methods=['POST'])
    def insert_property():
        try:
            property_payload = request.get_json()
            if property_payload == {}:
               raise ValueError("No data to post the record!")
            else:
                inserted_property = property_services.insert_property(property_payload)
                return http_responses.successResponse(inserted_property)
                        
        except Exception as error:
            return http_responses.errorResponse(str(error))

    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['PUT'])
    def update_property(id):
        try:
            property_payload = request.get_json()
            updated_property = property_services.update_property(id, property_payload)
            if property_payload =={} and updated_property == None:
                raise ValueError("Updating failed, payload is empty!")
            else:
                return http_responses.successResponse(updated_property)
        
        except Exception as error:
            return http_responses.errorResponse(str(error))

    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['DELETE'])    
    def deactivate_property(id):
        try:
            deleted_property = property_services.deactivate_property(id)
            if deleted_property == None:
                raise ValueError("ID does not match with any records!")
            else:
                return http_responses.successResponse(deleted_property)
        
        except Exception as error:
            return http_responses.errorResponse(str(error))
        
    #This code provides a basic implementation of a Flask API endpoint for retrieving all properties from a MongoDB database. 
    #The jsonify function is used to create a JSON response that can be sent back to the client.
