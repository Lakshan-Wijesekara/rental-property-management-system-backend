from flask import jsonify, request #jsonify converts python objects into JSON format
from services.db_collections import CollectionsModel
from services.util_services import UtilService
from services.http_responses import HttpResponse
from flask_cors import cross_origin

class PropertyController:
    def __init__(self, model): #model parameter is the MongoDBModel class
        self.model = model
        collections_list = CollectionsModel() #Instance of dbcollections
        self.property_collection_name = collections_list.property_collection_name #Access the variable in dbcollection
        self.convert_properties = UtilService()
        self.http_responses = HttpResponse()
        self.property_collection = model.get_propertyCollection(self.property_collection_name)

    @cross_origin(supports_credentials=True)
    def get_properties(self):
        try:
            get_property_collection =  self.property_collection
            properties = get_property_collection.find() #This returns a cursor object if not for list keyword(better for large datasets)
            json_properties = self.convert_properties.convert_cursor_object(properties)
            retrieve_all_response = self.http_responses.successResponse(json_properties)
            # Query parameters for filtering
            selectedCity = request.args.get('selectedCity')
            propertyName = request.args.get('propertyName')
            if selectedCity or propertyName:
                # Argument gets the selectedCity and propertyName from the URL and checks if the returned value can be found in the document list
                filter_query = {}
                if selectedCity:
                    filter_query['selectedCity'] = {"$regex": f"^{selectedCity}", "$options": "i"} #Here, f is the F string where the string to be more concise, ^ is the start of string, options make the filter not case sensitive
                if propertyName:
                    filter_query['propertyName'] = {"$regex": f"^{propertyName}", "$options": "i"}
                filter_query['is_active'] = True
                results = get_property_collection.find(filter_query)
                json_results = self.convert_properties.convert_cursor_object(results)
                filter_response = self.http_responses.successResponse(json_results)
                counter = get_property_collection.count_documents(filter_query)

                if counter>0:
                    return jsonify(filter_response)
                else:
                    return jsonify([])
                
            else:
                 return jsonify(retrieve_all_response)
        except Exception as error:
            error_at_exception = self.http_responses.errorResponse(str(error))
            return jsonify(error_at_exception)

    @cross_origin(supports_credentials=True)    
    def get_property(self,id):
        try:
            get_property_collection =  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            retrieved_property = get_property_collection.find({'_id': property_id}) 
            if retrieved_property:
                retrieved_property_object = self.convert_properties.convert_cursor_object(retrieved_property)
                success_response = self.http_responses.successResponse(retrieved_property_object)
                return jsonify(success_response)
            else:
                error_message = "Property id does not match with any records!"
                error_response = self.http_responses.errorResponse(error_message)
                return jsonify(error_response)
        except Exception as error:
            error_at_exception = self.http_responses.errorResponse(str(error))
            return jsonify(error_at_exception)   

    @cross_origin(supports_credentials=True)
    def insert_property(self):
        try:
            get_property_collection =  self.property_collection
            property_payload = request.get_json()
            inserted_property = get_property_collection.insert_one(property_payload)
            if inserted_property:
                inserted_property_id = str(inserted_property.inserted_id)
                success_response = self.http_responses.successResponse(inserted_property_id)
                return jsonify(success_response)
            else:
                error_message = "No document is available to insert!"
                error_response = self.http_responses.errorResponse(error_message)
                return jsonify(error_response)
        except Exception as error:
            error_at_exception = self.http_responses.errorResponse(str(error))
            return jsonify(error_at_exception)
        
    @cross_origin(supports_credentials=True)
    def update_property(self):
        try:
            get_property_collection =  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            property_payload = request.get_json()
            updated_property = get_property_collection.update_one({"_id": property_id}, {"$set":property_payload})
            if updated_property:
                success_message = "The identified property updated successfully"
                success_response = self.http_responses.successResponse(success_message)
                return jsonify(success_response)
            else:
                error_message = "No record found to update"
                error_response = self.http_responses.errorResponse(error_message)
                return jsonify(error_response)
        except Exception as error:
            error_at_exception = self.http_responses.errorResponse(str(error))
            return jsonify(error_at_exception)    

    @cross_origin(supports_credentials=True)    
    def deactivate_property(self, id):
        try:
            get_property_collection=  self.property_collection
            property_id = self.convert_properties.convert_object_id(id)
            deleted_property = get_property_collection.update_one({"_id": property_id},{"$set": {"is_active": False}})
            if deleted_property:
                success_message = "The identified property was deactivated successfully"
                success_response = self.http_responses.successResponse(success_message)
                return jsonify(success_response)
            else:
                error_message = "No record found to deactivate"
                error_response = self.http_responses.errorResponse(error_message)
                return jsonify(error_response)
        except Exception as error:
            error_at_exception = self.http_responses.errorResponse(str(error))
            return jsonify(error_at_exception)    
        
    #This code provides a basic implementation of a Flask API endpoint for retrieving all properties from a MongoDB database. 
    #The jsonify function is used to create a JSON response that can be sent back to the client.
