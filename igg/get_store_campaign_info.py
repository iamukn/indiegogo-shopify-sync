#!/usr/bin/python3
from requests import get
import os
from pprint import pprint

""" Function that gets the Volta Charger account campaign and info """

API_KEY = os.environ.get('igg_api_key')
ACCESS_TOKEN = os.environ.get('igg_access_token')
BASE_URL = os.environ.get('igg_base_url')

headers = {
    "accept": "application/json",
    "User-Agent": "curl",

        }

def get_store_campaigns_info(info:str="id"):
    global API_KEY, ACCESS_TOKEN, BASE_URL, headers
    url = BASE_URL + "/2/me.json"
    params = {
        "access_token": ACCESS_TOKEN,
        "api_token": API_KEY
            }

    try:
        res = get(url, params=params, headers=headers)
    except Exception:
        return "Cannot fetch campaigns"
    data = res.json()['response']
    if info == 'campaigns':
        return {'campaigns': data['campaigns']}
    return {'id': data['id']}
