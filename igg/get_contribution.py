#!/usr/bin/python3
from requests import post, get
from get_store_campaign_info import ACCESS_TOKEN, API_KEY, BASE_URL, headers



perks = []

def fetch_contribution(campaign_id, page):
    global perks
    # url to fetch campaigns
    url = BASE_URL + "/2/campaigns/%(campaign_id)s/contributions.json" %{'campaign_id': campaign_id}
    # params 
    params = {
            "api_token": API_KEY,
            "access_token": ACCESS_TOKEN,
            "page": page,
        }

    # Error handling
    try:
        # query the url to fetch contributions
        req = get(url, params=params, headers=headers)

        # set next page
        next_page = req.json().get('pagination').get('next')

        # return the response data
        
        res = req.json()['response']
        # loop through the response data and append to the list
        for response in res:

        #    if ("INDIE" not in response['order']['perks'][0]['label'].upper()):
        #        pass
            perks.append(response)
        
        if next_page == None:
            return perks
        # recursive call to the fetch contribution function
        fetch_contribution(campaign_id=campaign_id, page=next_page)
    except Exception as e:
        return "an error occurred in the fetch_contribution function"
    # return all perks
    return perks
