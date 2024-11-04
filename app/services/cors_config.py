from flask_cors import CORS

class CORSConfig:
    def __init__(self, origins="*", methods=["GET", "POST", "PUT", "DELETE"], headers=["Content-Type"]):
        self.origins = origins
        self.methods = methods
        self.headers = headers

    def initialize_cors(self, blueprint):
        CORS(blueprint, resources={
           r"/api/*":{
               "origins": self.origins,
               "methods": self.methods,
               "allow_headers": self.headers
           } 
        })