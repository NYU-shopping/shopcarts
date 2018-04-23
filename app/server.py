import sys
import logging
from flask import Flask, Response, jsonify, request, json, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from flasgger import Swagger
# from app.models import Item, DataValidationError
from app import app

#####################################################################
# Configure Swagger before initializing it
######################################################################
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "Swagger Shopcarts Service",
            "description": "This is a Shopcarts REST service.",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}
Swagger(app)

######################################################################
# Custom Exceptions
######################################################################
class DataValidationError(ValueError):
    pass

from app.models import *

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
# Routes
######################################################################

@app.route("/")
def home():
    return app.send_static_file('index.html')

######################################################################
# GET INDEX
######################################################################
@app.route('/shopcarts')
def index():
    """ Send back the home page """
    return app.send_static_file('index.html')

######################################################################
# LIST ALL ITEMS
######################################################################
@app.route('/shopcarts/items', methods=['GET'])
def list_items():
    """
    Returns all of the Items
    This endpoint will return all items unless a query parameter is specified
    ---
    tags:
      - Items
    description: The Items endpoint allows you to query Items
    parameters:
      - name: sku
        in: query
        description: the sku of the item you are looking for
        required: false
        type: string
      - name: name
        in: query
        description: the name of the item you are looking for
        required: false
        type: string
      - name: price
        in: query
        description: the minimum price of the item you are looking for
        required: false
        type: number
      - name: is_available
        in: query
        description: the availability of the item you are looking for
        required: false
        type: boolean
      - name: brand_name
        in: query
        description: the brand of the item you are looking for
        required: false
        type: string
    definitions:
      Item:
        type: object
        properties:
          id:
            type: integer
            description: unique ID assigned interally by service
          sku:
            type: string
            description: sku of the item
          name:
            type: string
            description: name of the item
          price:
            type: number
            description: price of the item
          is_available:
            type: boolean
            description: availability of the item
          brand_name:
            type: string
            description: brand of the item
          count:
            type: number
            description: quantity of the item
          link:
            type: string
            description: URL of the item
    responses:
      200:
        description: An array of Items
        schema:
            type: array
            items:
                schema:
                    $ref: '#/definitions/Item'
    """
    items = []
    sku = request.args.get('sku')
    name = request.args.get('name')
    price = request.args.get('price')
    is_available = request.args.get('is_available')
    brand_name = request.args.get('brand_name')
    if sku:
        items = Item.find_by_sku(sku)
    elif name:
        items = Item.find_by_name(name)
    elif price:
        items = Item.find_by_price(price)
    elif is_available:
        items = Item.find_by_availability(is_available)
    elif brand_name:
        items = Item.find_by_brand(brand_name)
    else:
        items = Item.all()

    results = [item.serialize() for item in items]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A ITEM
######################################################################
@app.route('/shopcarts/items/<int:item_id>', methods=['GET'])
def get_items(item_id):
    """
    Retrieve a single Item
    This endpoint will return an Item based on its id
    ---
    tags:
      - Items
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: ID of item to retrieve
        type: integer
        required: true
    responses:
      200:
        description: Item returned
        schema:
          $ref: '#/definitions/Item'
      404:
        description: Item not found
    """
    item = Item.find(item_id)
    if not item:
        abort(status.HTTP_404_NOT_FOUND, "Item with id '{}' was not found.".format(item_id))
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW ITEM
######################################################################
@app.route('/shopcarts/items', methods=['POST'])
def create_items():
    """
    Creates an Item
    This endpoint will create an Item based on the data in the body that is
    posted
    ---
    tags:
        - Items
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - in: body
          name: body
          required: true
          schema:
            id: data
            required:
                - sku
                - name
                - brand_name
                - price
                - count
                - is_available
                - link
            properties:
                sku:
                    type: string
                    description: enter sku of the item
                name:
                    type: string
                    description: enter name of the item
                brand_name:
                    type: string
                    description: enter brand of the item
                price:
                    type: number
                    description: enter price of the item
                count:
                    type: integer
                    description: enter quantity of the item
                is_available:
                    type: boolean
                    description: enter availability of the item
                link:
                    type: string
                    description: enter URL of the item
    responses:
        201:
            description: Item created
            schema:
                properties:
                    sku:
                        type: String
                        description: unique id assigned internally by service
                    name:
                        type: String
                        description: The name of the item in the system
                    brand_name:
                        type: String
                        description: The brand of the item in the system
                    price:
                        type: number
                        description: The price of the item in the system
                    count:
                        type: integer
                        description: The quantiyu of the item in the system
                    is_available:
                        type: boolean
                        description: The availability of the item in the system
                    link:
                        type: string
                        description: The URL of the item in the system
        400:
            description: Bad Request
    """
    data = {}
    # Check for form submission data
    app.logger.info('Processing JSON data')
    data = request.get_json()
    item = Item()
    item.deserialize(data)
    item.save()
    message = item.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {'Location': url_for('get_items', item_id=item.id, _external=True)})

######################################################################
# UPDATE AN EXISTING ITEM
######################################################################
@app.route('/shopcarts/items/<int:item_id>', methods=['PUT'])
def update_items(item_id):
    """
    Update an Item
    This endpoint will update an Item based on the data in the body that is
    posted
    ---
    tags:
        - Items
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - name: id
          in: path
          description: ID of the item to retrieve
          type: integer
          required: true
        - name: sku
          in: path
          description: sku of the item
          type: string
          required: true
        - name: name
          in: path
          description: name of the item
          type: string
          required: true
        - name: brand_name
          in: path
          description: brand of the item
          type: string
          required: true
        - name: price
          in: path
          description: price of the item
          type: number
          required: true
        - name: count
          in: path
          description: quantity of the item
          type: integer
          required: true
        - name: is_available
          in: path
          description: availability of the item
          type: boolean
          required: true
        - name: link
          in: path
          description: URL of the item
          type: string
          required: true
    responses:
        200:
            description: Item field updated
            schema:
                id: Item
                properties:
                    sku:
                        type: String
                        description: unique id assigned internally by service
                    name:
                        type: String
                        description: The name of the item in the system
                    brand_name:
                        type: String
                        description: The brand of the item in the system
                    price:
                        type: number
                        description: The price of the item in the system
                    count:
                        type: integer
                        description: The quantiyu of the item in the system
                    is_available:
                        type: boolean
                        description: The availability of the item in the system
                    link:
                        type: string
                        description: The URL of the item in the system
        400:
            description: Bad Request
    """
    item = Item.find_or_404(item_id)
    item.deserialize(request.get_json())
    item.id = item_id
    item.save()
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A ITEM
######################################################################
@app.route('/shopcarts/items/<int:item_id>', methods=['DELETE'])
def delete_items(item_id):
    """
    Delete an Item
    This endpoint will delete an Item based on the id specified in the path
    ---
    tags:
        - Items
    description: Deletes an Item from the database
    parameters:
      - name: id
        in: path
        description: ID of item to delete
        type: integer
        required: true
    responses:
        204:
            description: Item deleted
    """
    item = Item.find(item_id)
    if item:
        item.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
# (ACTION) DELETE ALL ITEMS
######################################################################
@app.route('/shopcarts/clear', methods=['DELETE'])
def delete_all_items():
    """
    Delete all items

    This is an action endpoint which clears the shopcart
    """
    Item.query.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    Item.init_db()

#@app.before_first_request
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
