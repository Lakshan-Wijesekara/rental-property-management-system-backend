from bson import json_util #Module used to serialize and deserialize BSON objects to and from JSON
from bson.objectid import ObjectId
import json #Module to work with JSON data

class PropertyService:
    def convert_cursor_object(self, cursorObject):
        properties = cursorObject
        properties_json = json_util.dumps(properties)
        properties_objects = json.loads(properties_json)
        return properties_objects
    
    def convert_object_id(self, id):
        property_id = id
        converted_id = ObjectId(property_id)
        return converted_id
    
# properties_json = json_util.dumps(properties) #To get the JSON string
# (because the cursor object cannot directly convert to objects)
# properties_objects = json.loads(properties_json) #Convert to JSON objects
# It uses the bson.json_util module to handle the conversion between BSON and JSON, ensuring that the data can be correctly serialized and deserialized. 
