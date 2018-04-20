"""
VCAP Services module

This module initializes the database connection String
from VCAP_SERVICES in Bluemix if Found
"""
import os
import json
import logging

def get_database_uri():
    """
        Initialized MySQL database connection
    """
    # Get the credentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        logging.info("Using VCAP_SERVICES...")
        vcap_services = os.environ['VCAP_SERVICES']
        services = json.loads(vcap_services)
        creds = services['cleardb'][0]['credentials']
        username = creds["username"]
        password = creds["password"]
        hostname = creds["hostname"]
        port = creds["port"]
        name = creds["name"]
    elif 'TRAVIS' in os.environ:
        logging.info("Using Travis")
        username = 'root'
        password = ''
        hostname = 'localhost'
        port = '3306'
        name = 'development'
    else:
        logging.info("Using localhost database...")
        username = 'root'
        password = 'passw0rd'
        hostname = 'localhost'
        port = '3306'
        name = 'development'

    logging.info("Conecting to database on host %s port %s", hostname, port)

    if password == '':
        connect_string = 'mysql+pymysql://{}@{}:{}/{}'
        return connect_string.format(username, hostname, port, name)
    else:
        connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}'
        returning_connect_string = connect_string.format(username, password, hostname, port, name)
        logging.info("DB URI %s", returning_connect_string)
        #return connect_string.format(username, password, hostname, port, name)
        return returning_connect_string
