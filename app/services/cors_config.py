from flask_cors import CORS
class CORSConfig:
    def __init__(self, origins="*", methods=["GET", "POST", "PUT", "DELETE"], headers=["Content-Type"], supports_credentials=False):
        self.origins = origins
        self.methods = methods
        self.headers = headers
        self.supports_credentials = supports_credentials

    def initialize_cors(self, blueprint):
        CORS(blueprint, resources={
           r"/api/*":{
               "origins": self.origins,
               "methods": self.methods,
               "allow_headers": self.headers,
               "expose_headers": ["NewAuthToken"],
           } 
        }, supports_credentials=self.supports_credentials)