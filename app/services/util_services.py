from bson.objectid import ObjectId

class UtilService:
    def convert_cursor_object(self, cursorObject):
        properties = cursorObject
        properties_list = list(properties)
        # Creates a list of dictionaries from properties_list and each is a copy of the original but the id is converted to a string id
        data_list = [{**doc, '_id': str(doc['_id'])} for doc in properties_list] 
        return data_list
    
    def convert_object_id(self, id):
        return ObjectId(id)
    
# properties_json = json_util.dumps(properties) #To get the JSON string
# (because the cursor object cannot directly convert to objects)
# properties_objects = json.loads(properties_json) #Convert to JSON objects
# It uses the bson.json_util module to handle the conversion between BSON and JSON, ensuring that the data can be correctly serialized and deserialized. 