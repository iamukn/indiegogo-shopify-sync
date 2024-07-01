#!/usr/bin/python3
import requests
import sys
from pprint import pprint
import os

# Add shopify directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from shopify.customer.customer import BASE_URL, headers

""" Send a draft invoice """

def send_invoice(draft_order_id:int, draft_name:str, to:str) -> dict or str:
    """ requires a draft_order_id, draft_name and a receiver email """
    # sends an invoice to a customer 
    url = BASE_URL + f"/admin/api/2024-04/draft_orders/{draft_order_id}/send_invoice.json"

    data = { "draft_order_invoice":
            {
            "from": os.environ.get('volta_igg_email'),
            "to": to,
            "custom_message": "Kindly complete the purchase as soon as possible.",
            "subject": f"Volta Charger Invoice {draft_name}",
            }
        }
    try:
        res = requests.post(url, headers=headers, json=data)
        return res.json()
    except Exception as e:
        return "an error occured while trying to send an invoice"
