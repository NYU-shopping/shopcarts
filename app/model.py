import logging
from flask_sqlalchemy import SQLAlchemy
import os
import json
from . import db



class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Item(db.Model):
    """
    Class that represents an item in the shopping cart

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(63))
    count = db.Column(db.Integer)
    price = db.Column(db.Float)
    name = db.Column(db.String(63))
    link = db.Column(db.String(63))
    brand_name = db.Column(db.String(63))
    is_available = db.Column(db.Boolean())

    def __repr__(self):
        return '<Item %r>' % (self.name)

    def save(self):
        """
        Saves a Item to the data store
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Item from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Item into a dictionary """
        return {"id": self.id,
                "sku": self.sku,
                "name": self.name,
                "brand_name": self.brand_name,
                "price": self.price,
                "count": self.count,
                "is_available": self.is_available,
                "link": self.link
                }

    def deserialize(self, data):
        """
        Deserializes a Item from a dictionary

        Args:
            data (dict): A dictionary containing the Item data
        """
        try:
            self.sku = data['sku']
            self.name = data['name']
            self.brand_name = data['brand_name']
            self.price = data['price']
            self.count = data['count']
            self.is_available = data['is_available']
            self.link = data['link']
            self.name = data['name']
        except KeyError as error:
            raise DataValidationError('Invalid item: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid item: body of request contained' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
          """ Initializes the database session """
        Item.logger.info('Initializing database')
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """ Returns all of the Items in the database """
        Item.logger.info('Processing all Items')
        return Item.query.all()

    @staticmethod
    def find(item_id):
        """ Finds a Item by its ID """
        Item.logger.info('Processing lookup for id %s ...', item_id)
        return Item.query.get(item_id)

    @staticmethod
    def find_or_404(item_id):
        """ Find a Item by its id """
        Item.logger.info('Processing lookup or 404 for id %s ...', item_id)
        return Item.query.get_or_404(item_id)

    @staticmethod
    def find_by_name(name):
        """ Returns all Items with the given name

        Args:
            name(string): the name of the Items you want to match
        """
        Item.logger.info('Processing name query for %s ...', name)
        return Item.query.filter(Item.name == name)

    @staticmethod
    def find_by_sku(sku):
        """ Returns all items with the given SKU
        Args:
            sku(string): sku id: name of sku
        """
        Item.logger.info('Processing SKU query for %s ...', sku)
        return Item.query.filter(Item.sku == sku)

    @staticmethod
    def find_by_price(price):
        """ Returns all Items less than or equal to a given price

        Args:
            price(float): the max price of the Items you want to query against
        """
        Item.logger.info('Processing price query for %s ...', price)
        return Item.query.filter(Item.price <= price)

    @staticmethod
    def find_by_availability(is_available=True):
        """ Query that finds Items by their availability """
        """ Returns all Items by their availability

        Args:
            is_available(boolean): true for items that are available
        """
        Item.logger.info('Processing available query for %s ...', is_available)
        return Item.query.filter(Item.is_available == is_available)

    @staticmethod
    def find_by_brand(brand_name):
        """ Returns all Items with a given brand name

        Args:
            brand_name(string): the brand_name of the Items you want to match
        """
        Item.logger.info('Processing brand_name query for %s ...', brand_name)
        return Item.query.filter(Item.brand_name == brand_name)

