#!/usr/bin/python3
from requests import post, get
import os
from typing import Dict
from pprint import pprint

""" Creates a new customer on shopify """

ACCESS_TOKEN  = os.environ.get('shopify_access_token')
API_KEY = os.environ.get('shopify_api_key')
SECRET_KEY = os.environ.get('shopify_secret_key')
BASE_URL = "https://volta-charger.myshopify.com"
headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
          }


def create_customer(customer_data:Dict, email:str) -> Dict:
    url = "/admin/api/2024-04/customers.json"
    global headers
    name = customer_data.get('name').split(' ')
    data = {
        "first_name": name[0],
        "last_name": '' if len(name) == 1 else name[-1],
        "email": email,
        "verified_email":True,
        "phone": customer_data.get('phone_number'),
        "addresses": [
            {
                "address1": customer_data.get('address'),
                "city": customer_data.get('city'),
                "province": customer_data.get('state'),
                "phone": customer_data.get('phone_number'),
                "zip": customer_data.get('zipcode'),
                "first_name": name[0],
                "last_name": "" if len(name) == 1 else name[-1],
                "country": customer_data.get('country'),
                }
            ],
        "send_email_welcome":True,

            }
    customer = {"customer": data}

    res = post(BASE_URL + url, json=customer, headers=headers)
    json=res.json()
    return json

def get_customer_id(email:str=None):
    url = "/admin/api/2024-04/customers/search.json"
    params = {"query": email}
    global headers
    try:
        res = get(BASE_URL + url, params=params,headers=headers)
        if len(res.json().get('customers')) < 1:
            return {'status':404, 'details': 'NOT FOUND'}
        res = res.json()
        id = {'status': 200, 'details': 'FOUND', 'customer_id':res.get('customers')[0].get('id'), 'email': email}

        return id
    except Exception as e:
        print(e)
        return "an error occurred"

