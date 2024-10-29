from flask import jsonify #jsonify converts python objects into JSON format
from dbcollections import CollectionsModel
from propertyservice import PropertyService

class PropertyController:
    def __init__(self, model): #model parameter is the MongoDBModel class
        self.model = model
        collections_list = CollectionsModel() #Instance of dbcollections
        self.property_collection = collections_list.propertyCollection #Access the variable in dbcollection
        self.convert_properties = PropertyService()

    def get_properties(self):
        try:
            get_property_collection = self.model.get_propertyCollection(self.property_collection)
            properties = get_property_collection.find() #This returns a cursor object
            # Convert a cursor objects to a JSON objects
            if properties:
                properties_objects = self.convert_properties.convert_cursor_object(properties)
                return jsonify(properties_objects), {'Access-Control-Allow-Origin': '*'}
            else:
                return {"error": "Could not find the properties"}
        except Exception as error:
            return {"error": "Property retrieving failed!"}
        
    def get_property(self,id):
        try:
            get_property_collection = self.model.get_propertyCollection(self.property_collection)
            property_id = self.convert_properties.convert_object_id(id)
            retrieved_property = get_property_collection.find_one({'_id': property_id}) 
            if retrieved_property:
                retrieved_property_object = self.convert_properties.convert_cursor_object(retrieved_property)
                return jsonify(retrieved_property_object)
            else:
                return {"error": "Property id does not match with any records!"}
        except Exception as error:
            return {"error": "invalid id"}        
    #This code provides a basic implementation of a Flask API endpoint for retrieving all properties from a MongoDB database. 
    #The jsonify function is used to create a JSON response that can be sent back to the client.
