#!/usr/bin/python3
from requests import post, get
from get_store_campaign_info import ACCESS_TOKEN, API_KEY, BASE_URL, headers

""" fetch a campaign perks linked to a campaign id """


def get_campaign_perks(campaign_id:str):
    # get a  perk
    url = BASE_URL + "/2/campaigns/%(campaign_id)s/perks.json" %{'campaign_id': campaign_id}
    params = {
        "api_token": API_KEY
            }
    
    try:
        res = get(url, headers=headers, params=params)
        print(res.json())
    except Exception:
        return "Unable to fetch perks"
get_campaign_perks('2618699')
