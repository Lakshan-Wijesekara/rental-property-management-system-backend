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
            property_collection =  self.property_collection
            # Query parameters for filtering
            filter_query = {}
            if selectedCity or propertyName:
                # Argument gets the selectedCity and propertyName from the URL and checks if the returned value can be found in the document list
                if selectedCity:
                    filter_query['selectedCity'] = {"$regex": f"^{selectedCity}", "$options": "i"} #Here, f is the F string where the string to be more concise, ^ is the start of string, options make the filter not case sensitive
                if propertyName:
                    filter_query['propertyName'] = {"$regex": f"^{propertyName}", "$options": "i"}
                filter_query['is_active'] = True

            properties = property_collection.find(filter_query)
            #This returns a cursor object if not for list keyword(better for large datasets)
            json_properties = self.convert_properties.convert_cursor_object(properties)
            counter = len(json_properties)
            if counter>0:
                return json_properties
            else:
                return jsonify([])
        except:
            raise

    def get_property(self,id):
        try:    
            property_collection =  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            retrieved_property = property_collection.find({'_id': property_id}) 
            retrieved_property_object = self.convert_properties.convert_cursor_object(retrieved_property)
            if retrieved_property:
                return retrieved_property_object
            else:
                error_message = "Property id does not match with any records!"
                return error_message
        except:
            raise
    
    def insert_property(self, property_payload):
        try:
            property_collection =  self.property_collection
            inserted_property = property_collection.insert_one(property_payload)
            inserted_property_id = str(inserted_property.inserted_id)
            if inserted_property:
                return inserted_property_id
            else:
                error_message = "No document is available to insert!"
                return error_message
        except:
            raise
    
    def update_property(self,id, property_payload):
        try:
            property_collection =  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            updated_property = property_collection.update_one({"_id": property_id}, {"$set":property_payload})
            if updated_property:
                success_message = "The identified property updated successfully"
                return success_message
            else:
                error_message = "No record found to update"
            return error_message 
        except:
            raise 
        
    def deactivate_property(self, id):
        try:
            property_collection=  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            deleted_property = property_collection.update_one({"_id": property_id},{"$set": {"is_active": False}})
            if deleted_property:
                success_message = "The identified property was deactivated successfully"
                return success_message
            else:
                error_message = "No record found to deactivate"
                return error_message
        except:
            raise 
              