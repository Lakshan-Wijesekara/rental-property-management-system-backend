from flask import Flask, jsonify
from controllers.property_controller import property_api_blueprint
from controllers.user_controller import user_api_blueprint
from services.exceptions import InvalidResponse

#Flask application instance named mongo_app
mongo_app = Flask(__name__) 
#Register the blueprint with main
mongo_app.register_blueprint(property_api_blueprint, url_prefix='/api')#All URLs defined at the blueprint will be prefixed with /api
mongo_app.register_blueprint(user_api_blueprint, url_prefix='/api')



#Ensures that the code within this block only runs when script is executed directly, not when imported as a module
if __name__== '__main__': 
    mongo_app.run(debug=True)