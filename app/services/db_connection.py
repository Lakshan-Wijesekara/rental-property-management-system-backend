#To connect the MongoDB database
import pymongo #Interface to interact with MongoDB
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')
Mongo_uri = os.getenv("DB_URI")
#Collection variables
property_collection_name = "property_details"

class MongoDBConnection:
    def __init__(self): #Base class
        self.client = pymongo.MongoClient(Mongo_uri)
        self.db = self.client['Property_Database']

    def get_propertyCollection(self, property_details):       
        propertyCollection = self.db[property_details]
        return propertyCollection

