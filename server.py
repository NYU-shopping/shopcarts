import os
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status
from werkzeug.exceptions import NotFound

app = Flask(__name__)

"""
    Required to set the port in order to access the server
    outside vagrant
"""
PORT = os.getenv('PORT', '5000')

####################
# GET INDEX (/)
####################
@app.route('/')
def index():
    return jsonify(name='Shopcarts REST API Service',
                   version='1.0'
                  ), status.HTTP_200_OK

############################################################
# GET ALL ITEMS IN THE SHOPCART (GET /shopcarts/items)
############################################################
@app.route('/shopcart/items', methods=['GET'])
def list_items():
    items = []

    it1 = {'name': 'nescafe', 'type': 'beverage', 'id': 1}
    it2 = {'name': 'lays', 'type': 'food', 'id': 2}
    it3 = {'name': 'ajax', 'type': 'cleaning', 'id': 3}

    items.append(dict(it1))
    items.append(dict(it2))
    items.append(dict(it3))

    return make_response(jsonify(items), status.HTTP_200_OK)

############################################################
# GET AN ITEM BY ID (GET /shopcarts/items/<item_id>)
############################################################
@app.route('/shopcart/items/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    items = []

    it1 = {'name': 'nescafe', 'type': 'beverage', 'id': 1}
    it2 = {'name': 'lays', 'type': 'food', 'id': 2}
    it3 = {'name': 'ajax', 'type': 'cleaning', 'id': 3}

    items.append(dict(it1))
    items.append(dict(it2))
    items.append(dict(it3))

    result = {}

    for item in items:
        if item['id'] == item_id:
            result = item

    if not result:
        raise NotFound("Item with id '{}' was not found.".format(item_id))

    return make_response(jsonify(result), status.HTTP_200_OK)

############################################################
# CREATE A NEW ITEM (POST /shopcart/items)
############################################################
@app.route('/shopcart/items', methods=['POST'])
def create_item():
    check_content_type('application/json')

    items = []

    it1 = {'name': 'nescafe', 'type': 'beverage', 'id': 1}
    it2 = {'name': 'lays', 'type': 'food', 'id': 2}
    it3 = {'name': 'ajax', 'type': 'cleaning', 'id': 3}

    items.append(dict(it1))
    items.append(dict(it2))
    items.append(dict(it3))

    new_item = request.get_json()

    items.append(new_item)
    new_item_id = len(items)
    new_item['id'] = new_item_id

    location_url = url_for('get_item_by_id', item_id=new_item_id, _external=True)
    return make_response(jsonify(new_item), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })

############################################################
# DELETE A ITEM (DELETE /shopcart/items)
############################################################
@app.route('/shopcart/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    app.logger.info('Request to delete Item with item_id:{}'.format(item_id))
    item = Item.find(item_id)
    if item:
        item.delete()
    return make_response(' ', status.HTTP_204_NO_CONTENT)

def check_content_type(content_type):
    print request.headers['Content-Type']
    if request.headers['Content-Type'] == content_type:
        return

    abort(415, 'Content-Type must be {}'.format(content_type))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT))
