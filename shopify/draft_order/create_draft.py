#!/usr/bin/python3
import requests
import sys
from pprint import pprint
import os
from typing import List, Dict

# Add shopify directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from shopify.customer.customer import BASE_URL, headers, create_customer, get_customer_id
from shopify.product.products import get_variant_id
from shopify.draft_order.send_an_invoice import send_invoice
from database.db_connect import User, session

""" creating a draft order """
def create_draft(order: List, email:str) -> Dict:
    email = email
    order = order
    # set the payload
    payload = {
        "draft_order": {
            "line_items": [],
            }
            }
    url = BASE_URL + "/admin/api/2024-04/draft_orders.json"
    try:
        # loop through the perk to add all products 
        for perk in order.get('perks'):
            for item in perk.get('items'):
                perk_item = item
                perk_name = perk_item.get('name')
                perk_quantity = perk_item.get('quantity')
                variant_id =  get_variant_id(name=perk_name).get('variant')
                order_data = {
                    "variant_id": variant_id,
                    "quantity": perk_quantity,
                    "applied_discount": {
                    "description": "IGG Contribution",
                    "value": "100.00",
                    "value_type": "percentage",
                    "amount": "0.00",
                    "title": "Paid on indiegogo",
                        }
                    }
                payload.get('draft_order').get('line_items').append(order_data)
        payload['draft_order']['note'] = 'Contribution %(id)s' %{'id': order.get('sequence_number')}

            
        # shipping address
        shipping_data = order.get('shipping')
        name = shipping_data.get('name').split(' ')
        shipping_address = {
            "first_name": name[0],
            "last_name": '' if len(name) == 1 else name[1],
            "address1": shipping_data.get('address', ''),
            "phone": shipping_data.get('phone_number', ''),
            "city": shipping_data.get('city', ''),
            "province": shipping_data.get('state', ''),
            "country": shipping_data.get('country', ''),
            "zip":shipping_data.get('zipcode', ''),
                }

        shipping_line = {
            "title": "Free shipping",
            "price": "0.00",
            "code": "Indiegogo"
                }

        tags = "draft"
        
        # add to draft order payloads
        payload['draft_order']['shipping_line'] = shipping_line
        payload['draft_order']['tags'] = tags
        payload['draft_order']['shipping_address'] = shipping_address
        payload['draft_order']['use_customer_default_address'] = False
        # get customer id if customer exist
        customer_id = get_customer_id(email=email)
        # check if customer exists
        if customer_id.get('status') == 200:
            payload['draft_order']['customer'] = {
                "id": customer_id.get('customer_id'),
                    }
        else:
            # creates a new customer if the customer doesn't exist
            customer_data = {
                "name": shipping_data.get('name', ''),
                "address": shipping_data.get('address', ''),
                "city": shipping_data.get('city', ''),
                "province": shipping_data.get('state', ''),
                "zipcode": shipping_data.get('zipcode'),
                "country": shipping_data.get('country'),
                    }
            try:
                
                new_customer = create_customer(customer_data=customer_data,email=email)
                new_id = new_customer.get('customer').get('id')
                payload['draft_order']['customer'] = {
                        "id": new_id,
                        }
            except Exception as e:
                print(e)
                return "Error creating a new customer"

        # create the draft order
        res = requests.post(url, json=payload, headers=headers)

        if res.status_code == 202 or res.status_code == 201:

            # update the database with the email and contribution id

            draft_info = res.json()['draft_order']
            draft_info = {'draft_id': draft_info.get('id'), 'draft_name': draft_info.get('name'), 'draft_email': draft_info.get('email')}
            
            # Send an invoice to the customer
            send_email = send_invoice(draft_order_id=draft_info.get('draft_id'), draft_name=draft_info.get('draft_name'), to=draft_info.get('draft_email'))
            # update the database with the email and contribution id
            new_user_data = User(email=email, contribution_id=order.get('sequence_number'))
            session.add(new_user_data)
            session.commit()
            return "Sent"
    
    except Exception as e:
        print(e)
