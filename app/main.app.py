from flask import Flask
from controllers.property_controller import api_blueprint

#Flask application instance named mongo_app
mongo_app = Flask(__name__) 
#Register the blueprint with main
mongo_app.register_blueprint(api_blueprint, url_prefix='/api')

#Ensures that the code within this block only runs when script is executed directly, not when imported as a module
if __name__== '__main__': 
    mongo_app.run(debug=True)