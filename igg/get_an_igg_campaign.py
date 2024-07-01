#!/usr/bin/python3
from requests import post, get
from get_store_campaign_info import ACCESS_TOKEN, API_KEY, BASE_URL, headers

""" fetch all campaigns linked to an id """

def get_a_campaign(campaign_id: str):
    # get a campaign using the campaign ID

    url = BASE_URL + "/2/campaigns.json"

    try:
        params = {
            "api_token": API_KEY,
            "ids[]": str(campaign_id)
                }
        res = get(url, params=params, headers=headers)
        return res.json()
    except Exception as e:
        print(e)
        return "Couldn't get campaigns"

print(get_a_campaign('2618699'))
