import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy

from model import Item, DataValidationError

# Create Flask application
app = Flask(__name__)

# We'll just use SQLite here so we don't need an external database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'please, tell nobody... Shhhh'
app.config['LOGGING_LEVEL'] = logging.INFO

# Initialize SQLAlchemy
#db = SQLAlchemy(app)

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=400, error='Bad Request', message=message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=404, error='Not Found', message=message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=405, error='Method not Allowed', message=message), 405

@app.errorhandler(415)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=415, error='Unsupported media type', message=message), 415

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=500, error='Internal Server Error', message=message), 500


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return jsonify(name='Shopcarts REST API Service',
                   version='1.0',
                   paths=url_for('list_items', _external=True)
                  ), status.HTTP_200_OK

######################################################################
# LIST ALL ITEMS
######################################################################
@app.route('/items', methods=['GET'])
def list_items():
    """ Returns all of the Items """
    items = []
    sku = request.args.get('sku')
    name = request.args.get('name')
    brand_name = request.args.get('brand_name')
    if sku:
        items = Item.find_by_sku(sku)
    elif name:
        items = Item.find_by_name(name)
    elif brand_name:
        items = Item.find_by_brand(brand_name)
    else:
        items = Item.all()

    results = [item.serialize() for item in items]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A ITEM
######################################################################
@app.route('/items/<int:item_id>', methods=['GET'])
def get_items(item_id):
    """
    Retrieve a single Item

    This endpoint will return an Item based on it's id
    """
    item = Item.find(item_id)
    if not item:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW ITEM
######################################################################
@app.route('/items', methods=['POST'])
def create_items():
    """
    Creates an Item
    This endpoint will create an Item based the data in the body that is posted
    """
    check_content_type('application/json')
    item = Item()
    item.deserialize(request.get_json())
    item.save()
    message = item.serialize()
    location_url = url_for('get_items', item_id=item.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })


######################################################################
# UPDATE AN EXISTING ITEM
######################################################################
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_items(item_id):
    """
    Update an Item

    This endpoint will update a Item based the body that is posted
    """
    check_content_type('application/json')
    item = Item.find(item_id)
    if not item:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    item.deserialize(request.get_json())
    item.id = item_id
    item.save()
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A ITEM
######################################################################
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_items(item_id):
    """
    Delete an Item

    This endpoint will delete an Item based the id specified in the path
    """
    item = Item.find(item_id)
    if item:
        item.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Item.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "===================================================="
    print " S H O P C A R T S   S E R V I C E   S T A R T I N G"
    print "===================================================="
    initialize_logging(logging.INFO)
    init_db()  # make our sqlalchemy tables
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
