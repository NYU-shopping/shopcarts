"""
Shopcart Steps

Steps file for Shopcart.feature
"""

from os import getenv
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from app import server

WAIT_SECONDS = 30
BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@given(u'the following items')
def step_impl(context):
    """ Delete all items and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/shopcarts/clear', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/shopcarts/items'
    for row in context.table:
        data = {
            "sku": row['sku'],
            "name": row['name'],
            "brand_name": row['brand_name'],
            "price": row['price'],
            "count": row['count'],
            "is_available": row['is_available'],
            "link": row['link']
            }

        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)

@when(u'I visit the "Cart page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url + '/shopcarts')

@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)

@then(u'I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)
