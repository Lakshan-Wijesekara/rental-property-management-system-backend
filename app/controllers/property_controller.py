from flask import jsonify, request #jsonify converts python objects into JSON format
from services.db_collections import CollectionsModel
from services.util_services import UtilService

class PropertyController:
    def __init__(self, model): #model parameter is the MongoDBModel class
        self.model = model
        collections_list = CollectionsModel() #Instance of dbcollections
        self.property_collection = collections_list.propertyCollection #Access the variable in dbcollection
        self.convert_properties = UtilService()

    def get_properties(self):
        try:
            get_property_collection = self.model.get_propertyCollection(self.property_collection)
            properties = get_property_collection.find() #This returns a cursor object if not for list keyword(better for large datasets)
            json_properties = self.convert_properties.convert_cursor_object(properties)
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
                results = get_property_collection.find(filter_query)
                json_results = self.convert_properties.convert_cursor_object(results)
                counter = get_property_collection.count_documents(filter_query)

                if counter>0:
                    return jsonify(json_results), {'Access-Control-Allow-Origin': '*'}
                else:
                    return jsonify([]), {'Access-Control-Allow-Origin': '*'}
                
            else:
                 return jsonify(json_properties), {'Access-Control-Allow-Origin': '*'}
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

    def insert_property(self):
        try:
            get_property_collection= self.model.get_propertyCollection(self.property_collection)
            property_payload = request.get_json()
            inserted_property = get_property_collection.insert_one(property_payload)
            if inserted_property:
                inserted_property_id = str(inserted_property.inserted_id)
                return {"message":"Property added succesfully", "id":inserted_property_id}
            else:
                return {"error": "No document is available to insert"}
        except:
            return {"error": "Error occurred during operation"}     

    def update_property(self, id):
        try:
            get_property_collection= self.model.get_propertyCollection(self.property_collection)
            property_id = self.convert_properties.convert_object_id(id)
            property_payload = request.get_json()
            updated_property = get_property_collection.update_one({"_id": property_id}, {"$set":property_payload})
            if updated_property:
                return {"message":"Property updated succesfully"}
            else:
                return {"error": "No record found to update"}
        except:
            return {"error": "Error occurred during update operation"}     
    #This code provides a basic implementation of a Flask API endpoint for retrieving all properties from a MongoDB database. 
    #The jsonify function is used to create a JSON response that can be sent back to the client.
