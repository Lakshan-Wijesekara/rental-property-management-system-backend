#To connect the MongoDB database
from pymongo import MongoClient #Import MongoClient to connect to a MongoDB Server
import pymongo #Interface to interact with MongoDB

class MongoDBModel:
    def __init__(self, uri): #Base class
        self.client = pymongo.MongoClient(uri)
        self.db = self.client['Property_Database']

    def get_propertyCollection(self, property_details):       
        propertyCollection = self.db[property_details]
        return propertyCollection