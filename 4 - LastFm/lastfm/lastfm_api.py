# !/usr/bin/env python3

import requests

BASE_URL = "http://ws.audioscrobbler.com/2.0/?method="

# Base method to make calls to the Last.FM API.
def _request(method, api_key, params = ''):
    requestUrl = f"{BASE_URL}{method}{params}&api_key={api_key}&format=json"

    return requests.get(requestUrl).json()

# Fetches the information of the given user.
def user_info(user, api_key):
    return _request('user.getinfo', api_key, params=f"&user={user}")


