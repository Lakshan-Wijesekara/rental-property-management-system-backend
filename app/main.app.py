from flask import Flask, Blueprint
from dotenv import load_dotenv
import os
from controllers.property_controller import PropertyController
from models.property_model import MongoDBModel
from services.cors_config import CORSConfig

mongo_app = Flask(__name__) #Flask application instance named mongo_app
#To load the URI from environment file,
load_dotenv(dotenv_path='.env')
#Set the URI,
Mongo_uri = os.getenv("DB_URI")
# MongoDB model instance created,
mongo_model = MongoDBModel(Mongo_uri) #Passing the Mongo_uri to the MongoDBModel class again is a common practice in object-oriented programming to ensure that each instance has the necessary information to connect to the desired MongoDB server. This approach promotes encapsulation, flexibility, and better code organization.
#PropertyController instance created,
property_controller = PropertyController(mongo_model)
#Create a Blueprint
api_blueprint = Blueprint('properties_api', __name__)
#Initialize CORS on blueprint
cors_config = CORSConfig(origins=["http://127.0.0.1:5000/api/properties"], headers=["Content-Type", "Authorization"])
cors_config.initialize_cors(api_blueprint)

@api_blueprint.route('/properties', methods=['GET']) #API endpoint
def get_properties():
    return property_controller.get_properties() 

@api_blueprint.route('/properties/<id>', methods=['GET']) #API endpoint
def get_one_property(id):
    return property_controller.get_property(id)

@api_blueprint.route('/properties', methods=['POST']) #API endpoint
def insert_one_property():
    return property_controller.insert_property() 

@api_blueprint.route('/properties/<id>', methods=['PUT']) #API endpoint
def update_property(id):
    return property_controller.update_property(id) 

@api_blueprint.route('/properties/<id>', methods=['DELETE']) #API endpoint
def deactivate_property(id):
    return property_controller.deactivate_property(id) 

#Register the blueprint with main
mongo_app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__== '__main__': #Ensures that the code within this block only runs when script is executed directly, not when imported as a module
    mongo_app.run(debug=True)