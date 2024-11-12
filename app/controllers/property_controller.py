from flask import Blueprint #jsonify converts python objects into JSON format
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
        return property_services.get_all()
    
    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['GET'])    
    def get_property(id):
        return property_services.get_property(id)

    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties', methods=['POST'])
    def insert_property():
        return property_services.insert_property()
        
    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['PUT'])
    def update_property(id):
        return property_services.update_property(id)  

    @cross_origin(supports_credentials=True)
    @api_blueprint.route('/properties/<id>', methods=['DELETE'])    
    def deactivate_property(id):
        return property_services.deactivate_property(id)
        
    #This code provides a basic implementation of a Flask API endpoint for retrieving all properties from a MongoDB database. 
    #The jsonify function is used to create a JSON response that can be sent back to the client.
