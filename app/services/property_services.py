from flask import jsonify
from services.http_responses import HttpResponse
from services.util_services import UtilService
from services.db_connection import MongoDBConnection, property_collection_name


class PropertyServices:
    def __init__(self): #model parameter is the MongoDBModel class
        database_connection = MongoDBConnection()
        self.convert_properties = UtilService()
        self.http_responses = HttpResponse()
        self.property_collection = database_connection.get_propertyCollection(property_collection_name)

    def get_all(self,selectedCity, propertyName):
        try:
            get_property_collection =  self.property_collection
            # Query parameters for filtering
            filter_query = {}
            if selectedCity or propertyName:
                # Argument gets the selectedCity and propertyName from the URL and checks if the returned value can be found in the document list
                if selectedCity:
                    filter_query['selectedCity'] = {"$regex": f"^{selectedCity}", "$options": "i"} #Here, f is the F string where the string to be more concise, ^ is the start of string, options make the filter not case sensitive
                if propertyName:
                    filter_query['propertyName'] = {"$regex": f"^{propertyName}", "$options": "i"}
                filter_query['is_active'] = True

            properties = get_property_collection.find(filter_query)
            #This returns a cursor object if not for list keyword(better for large datasets)
            json_properties = self.convert_properties.convert_cursor_object(properties)
            retrieve_all_response = self.http_responses.successResponse(json_properties)
            counter = len(json_properties)
            if counter>0:
                return retrieve_all_response
            else:
                return jsonify([])
        except Exception as error:
            return self.http_responses.errorResponse(str(error))
    
    def get_property(self,id):
        try:    
            get_property_collection =  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            retrieved_property = get_property_collection.find({'_id': property_id}) 
            retrieved_property_object = self.convert_properties.convert_cursor_object(retrieved_property)
            return retrieved_property_object
        except Exception as error:
            return self.http_responses.errorResponse(str(error))
    
    def insert_property(self, property_payload):
        try:
            get_property_collection =  self.property_collection
            inserted_property = get_property_collection.insert_one(property_payload)
            inserted_property_id = str(inserted_property.inserted_id)
            return inserted_property_id
        except Exception as error:
            return self.http_responses.errorResponse(str(error))
    
    def update_property(self,id, property_payload):
        try:
            get_property_collection =  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            updated_property = get_property_collection.update_one({"_id": property_id}, {"$set":property_payload})
            return updated_property
        except Exception as error:
            return self.http_responses.errorResponse(str(error))
        
    def deactivate_property(self, id):
        try:
            get_property_collection=  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            deleted_property = get_property_collection.update_one({"_id": property_id},{"$set": {"is_active": False}})
            return deleted_property
        except Exception as error:
            return self.http_responses.errorResponse(str(error))
              