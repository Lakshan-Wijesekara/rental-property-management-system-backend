from flask import Flask
from dotenv import load_dotenv
import os
from controllers.property_controller import PropertyController
from models.property_model import MongoDBModel

mongo_app = Flask(__name__) #Flask application instance named mongo_app
#To load the URI from environment file,
load_dotenv(dotenv_path='.env')
#Set the URI,
Mongo_uri = os.getenv("DB_URI")
# MongoDB model instance created,
mongo_model = MongoDBModel(Mongo_uri) #Passing the Mongo_uri to the MongoDBModel class again is a common practice in object-oriented programming to ensure that each instance has the necessary information to connect to the desired MongoDB server. This approach promotes encapsulation, flexibility, and better code organization.
#PropertyController instance created,
property_controller = PropertyController(mongo_model)

@mongo_app.route('/api/properties') #API endpoint
def get_properties():
    return property_controller.get_properties() 

@mongo_app.route('/api/properties/<id>') #API endpoint
def get_one_property(id):
    return property_controller.get_property(id)

@mongo_app.route('/api/properties', methods=['POST']) #API endpoint
def insert_one_property():
    return property_controller.insert_property() 

@mongo_app.route('/api/properties/<id>', methods=['PUT']) #API endpoint
def update_property(id):
    return property_controller.update_property(id) 

if __name__== '__main__': #Ensures that the code within this block only runs when script is executed directly, not when imported as a module
    mongo_app.run(debug=True)