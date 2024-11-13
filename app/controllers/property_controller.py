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
            retrieve_all = property_services.get_all(selectedCity, propertyName)
            retrieve_all_response = http_responses.successResponse(retrieve_all)
            return jsonify(retrieve_all_response)
        except Exception as error:
            error_at_exception = http_responses.errorResponse(str(error))
            return jsonify(error_at_exception)
        
    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['GET'])    
    def get_property(id):
        try:
            retrieved_property = property_services.get_property(id)
            if retrieved_property:
                success_response = http_responses.successResponse(retrieved_property)
                return jsonify(success_response)
            else:
                error_message = "Property id does not match with any records!"
                error_response = http_responses.errorResponse(error_message)
                return jsonify(error_response)

        except Exception as error:
            error_at_exception = http_responses.errorResponse(str(error))
            return jsonify(error_at_exception)  

    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties', methods=['POST'])
    def insert_property():
        try:
            property_payload = request.get_json()
            inserted_property = property_services.insert_property(property_payload)
            if inserted_property:
                success_response = http_responses.successResponse(inserted_property)
                return jsonify(success_response)
            else:
                error_message = "No document is available to insert!"
                error_response = http_responses.errorResponse(error_message)
                return jsonify(error_response)
        except Exception as error:
            error_at_exception = http_responses.errorResponse(str(error))
            return jsonify(error_at_exception) 

    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['PUT'])
    def update_property(id):
        try:
            property_payload = request.get_json()
            updated_property = property_services.update_property(id, property_payload)
            if updated_property:
                success_message = "The identified property updated successfully"
                success_response = http_responses.successResponse(success_message)
                return jsonify(success_response)
            else:
                error_message = "No record found to update"
                error_response = http_responses.errorResponse(error_message)
            return jsonify(error_response)  
        except Exception as error:
            error_at_exception = http_responses.errorResponse(str(error))
            return jsonify(error_at_exception)

    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['DELETE'])    
    def deactivate_property(id):
        try:
            deleted_property = property_services.deactivate_property(id)
            if deleted_property:
                success_message = "The identified property was deactivated successfully"
                success_response = http_responses.successResponse(success_message)
                return jsonify(success_response)
            else:
                error_message = "No record found to deactivate"
                error_response = http_responses.errorResponse(error_message)
                return jsonify(error_response)
        
        except Exception as error:
            error_at_exception = http_responses.errorResponse(str(error))
            return jsonify(error_at_exception) 
        
    #This code provides a basic implementation of a Flask API endpoint for retrieving all properties from a MongoDB database. 
    #The jsonify function is used to create a JSON response that can be sent back to the client.
