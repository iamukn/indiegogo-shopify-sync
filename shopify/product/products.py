#!/usr/bin/python3
import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from shopify.customer.customer import BASE_URL, headers
from pprint import pprint
from typing import List

""" Fetch products variant """


def get_all_variants():
    url = BASE_URL + "/admin/api/2024-04/products.json"
    res = requests.get(url, headers=headers)
    products = res.json().get('products', [])
    


    result = []

    if len(products) == 0:
        return "No products available on this account"

    for product in products:

        if not product.get('variants')[0].get('sku'):
            pass
        if len(product.get('variants')) == 1:
            info = {
                "title": product.get('title'),
                "sku": product.get('variants')[0]['sku'],
                "variant": product.get('variants')[0]['id']
                }
            result.append(info)

        elif len(product.get('variants')) > 1:
            for variant in product.get('variants'):
                info = {
                        "title": product.get('title'),
                        "sku": variant.get('sku'),
                        "variant": variant.get('id')
                     } 
                result.append(info)
    return result if all(result) else "error occurred"


def get_variant_id(sku:str=None, name:str=None) -> dict: 
    variant = get_all_variants()

    if variant and sku:
        for var in variant:
            if not var.get('sku') or "FREE" in var.get('title').upper() or "REPLACEMENT" in var.get('title').upper(): pass
            elif var.get('sku').upper() == sku.upper():
                return var
            pass
    elif variant and name:
        for var in variant:
            if not var.get('title') or not var.get('sku') or "FREE" in var.get('title').upper() or "REPLACEMENT" in var.get('title').upper(): pass
            elif name.upper() in var.get('title').upper():
                return var

    return "No matched Name or SKU"
