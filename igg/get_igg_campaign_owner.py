#!/usr/bin/python3
from requests import post, get
from get_store_campaign_info import ACCESS_TOKEN, API_KEY, BASE_URL, headers, get_account_id

""" fetch all information about a campaign owner"""

def get_campaign_owner(campaign_id:str):
    # get campaign owner information

    url = BASE_URL + "/2/campaigns/%(id)s/owner.json" %{'id': campaign_id}
    params = {
        "api_token": API_KEY
            }
    try:
        res = get(url, headers=headers, params=params)
        print(res.json())
        return res.json()
    except Exception:
        return "Cannot get owners information"
get_campaign_owner('2676466')
