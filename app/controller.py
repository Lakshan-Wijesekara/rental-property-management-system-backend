from flask import jsonify #jsonify converts python objects into JSON format
from dbcollections import CollectionsModel
from propertyservice import PropertyService

class PropertyController:
    def __init__(self, model): #model parameter is the MongoDBModel class
        self.model = model
        collections_list = CollectionsModel() #Instance of dbcollections
        self.property_collection = collections_list.propertyCollection #Access the variable in dbcollection

    def get_properties(self):
        convert_properties = PropertyService()
        get_property_collection= self.model.get_propertyCollection(self.property_collection)
        properties = get_property_collection.find() #This returns a cursor object
        # Convert a cursor objects to a JSON objects
        properties_objects = convert_properties.convert_cursor_object(properties)
        return jsonify(properties_objects), {'Access-Control-Allow-Origin': '*'} 
    
    #This code provides a basic implementation of a Flask API endpoint for retrieving all properties from a MongoDB database. 
    #The jsonify function is used to create a JSON response that can be sent back to the client.
