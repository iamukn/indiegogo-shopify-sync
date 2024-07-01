#!/usr/bin/python3
from requests import post, get
from get_store_campaign_info import ACCESS_TOKEN, API_KEY, BASE_URL, headers
from get_contribution import fetch_contribution
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shopify.draft_order.create_draft import create_draft
from database.db_connect import User, session


""" fetch campaign contributions linked to a campaign id """
def get_contributions(campaign_id:str, page):
    # fetch all contributions linked to an id

    try:        
        req = fetch_contribution(campaign_id=campaign_id, page=page)
        
        if len(req) == 0:
            return {'status': 404, 'details': 'NOT FOUND'}

        # gets the contribution response
        response = req
        
        # loops through all the responses to get the data
        for res in response:
           
            if ("INDIE DROP" not in res['order']['perks'][0]['label'].upper()):
                continue

            
            contribution_id = res['order']['sequence_number']
            status = res['order']['status']
            email = res['email']
            
            # checks if this  contribution is already synced
            query = session.query(User).filter(User.email==email).filter(contribution_id==contribution_id).count()

            # syncs the contribution if it's not synced
            if query == 0:
                # check if the user is a shopify user
                try:
                    if status == 'in_fulfillment' or status == 'pending':
            
                        order = res.get('order')
                        # create a draft order
                        make_draft = create_draft(order=order, email=email)
                        
                        
                except Exception:
                    return "Database error"
            else:
                continue
    except Exception as e:
        print(e)
        return "Server Error"

get_contributions(campaign_id=2863364, page=1)
