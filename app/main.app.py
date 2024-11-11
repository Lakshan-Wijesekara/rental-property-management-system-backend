from flask import Flask
from controllers.property_controller import api_blueprint

mongo_app = Flask(__name__) #Flask application instance named mongo_app
#Register the blueprint with main
mongo_app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__== '__main__': #Ensures that the code within this block only runs when script is executed directly, not when imported as a module
    mongo_app.run(debug=True)