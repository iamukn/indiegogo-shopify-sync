#!/usr/bin/python3
from requests import post, get
from get_store_campaign_info import ACCESS_TOKEN, API_KEY, BASE_URL, headers
from get_contribution import fetch_contribution
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shopify.draft_order.create_draft import create_draft
from database.db_connect import User, session


""" fetch campaign contributions linked to a campaign id """
def get_contributions(campaign_id:str, page):
    # fetch all contributions linked to an id
    count = 0

    try:        
        # fetch all contribution using the campaign_id and the page number to fetch
        req = fetch_contribution(campaign_id=campaign_id, page=page)
        
        # returns a 404 if the page isn't found
        if len(req) == 0:
            return {'status': 404, 'details': 'NOT FOUND'}

        # gets the contribution response
        response = req
        # loops through all the responses to get the data
        for res in response:
            # skips the contribution with no order information
            if res is None or res['order'] is None or res['order']['perks'][0]['label'] is None:
                continue
            # skips contribution with no 'Indie' flag in their label
            elif ("INDIE" not in res['order']['perks'][0]['label'].upper()):
                continue
            # gets the contribution ID, status and email of backer
            contribution_id = res['order']['sequence_number']
            status = res['order']['status']
            email = res['email']
        
            # checks if this  contribution is already synced by confirming in the db
            query = session.query(User).filter(User.email==email).filter(User.contribution_id==contribution_id).count()
            # syncs the contribution if it's not synced
            if query == 0:
                try:
                    if status == 'in_fulfillment': #or status == 'pending': 
                        print('Creating order for {0}, please wait!'.format(email))
                        order = res.get('order')
                        # create a draft order
                        make_draft = create_draft(order=order, email=email)
                        # increment the order creation count and wait 2 seconds
                        count += 1
                        time.sleep(2)
                               
                except Exception as e:
                    print(e)
                    return "Database error"
        print(f'Draft created and invoice sent to {count} customers')
    except Exception as e:
        print(e)
        raise e 
        print('except block')
        return "Server Error"


# campaign IDs
campaign_id= {
        "VOLTAGO": 2863364,
        "TRAVELGO": 2856437,
        "200W": 2676466,
        }

# Get a campaign name from user
campaign = input('Enter the campaign product name: e.g TravelGo: ')

# get the campaign id if the campaign the user passed exists
if campaign.upper() in campaign_id:
    campaign_id = campaign_id.get(campaign.upper())
    print(f'Synchronizing perks for {campaign}! Please wait')
    get_contributions(campaign_id=campaign_id, page=1)
else:
    print('Could not find {} campaign!'.format(campaign))
