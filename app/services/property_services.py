from flask import jsonify
from services.http_responses import HttpResponse
from services.util_services import UtilService
from services.db_connection import MongoDBConnection, property_collection_name
from models.property_model import Property

class PropertyServices:
    def __init__(self): #model parameter is the MongoDBModel class
        database_connection = MongoDBConnection()
        self.convert_properties = UtilService()
        self.http_responses = HttpResponse()
        self.property_collection = database_connection.get_propertyCollection(property_collection_name)

    def get_all(self, selectedCity, propertyName):
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

    def get_property(self, id):
        try:    
            property_collection =  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            retrieved_property = property_collection.find({'_id': property_id}) 
            retrieved_property_object = self.convert_properties.convert_cursor_object(retrieved_property)
            if retrieved_property_object==[]:
                raise ValueError("No record found from the given ID!")
            else:
                return self.http_responses.successResponse(retrieved_property_object)
            
        except:
            raise
    
    def insert_property(self, property_payload ):
        property_collection =  self.property_collection
        #Unpacks the incoming dict to a Property model instance dataclass
        property_model_instance = Property(**property_payload)
        #Convert the incoming payload to a dictionary
        property_dict = property_model_instance.__dict__.copy()
        if property_payload == {}:
            raise ValueError("No data is available to post the record!")
        elif property_dict != {}:
            try:
                inserted_property = property_collection.insert_one(property_dict)
                inserted_property_id = str(inserted_property.inserted_id)
                return self.http_responses.successResponse(inserted_property_id)      
            except:
                raise
    
    def update_property(self, id, property_payload):
        try:
            property_collection =  self.property_collection
            property_model_instance = Property(**property_payload)
            property_dict = property_model_instance.__dict__.copy()
            property_id = self.convert_properties.convert_object_id(id)
            updated_property = property_collection.update_one({"_id": property_id}, {"$set":property_dict})
            if updated_property.matched_count==0 and property_payload == {}:
                raise ValueError("Id not found to update or no data to update the record!")
            else:
                return self.http_responses.successResponse(str(property_id))
        except:
            raise 
        
    def deactivate_property(self, id):
        try:
            property_collection=  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            deleted_property = property_collection.update_one({"_id": property_id},{"$set": {"is_active": False}})
            if deleted_property.matched_count==0 and id==None:
                raise ValueError("Given ID does not match with any records or id is not valid!")
            else:
                return self.http_responses.successResponse(str(property_id))  
        except:
            raise 
              