# !/usr/bin/env python3

import requests
from datetime import date, datetime, timedelta

BASE_URL = "http://ws.audioscrobbler.com/2.0/?method="

# Base method to make calls to the Last.FM API.
def _request(method, api_key, params = ''):
    requestUrl = f"{BASE_URL}{method}{params}&api_key={api_key}&format=json"

    return requests.get(requestUrl).json()

# Fetches the information of the given user.
def user_info(user, api_key):
    return _request('user.getinfo', api_key, params=f"&user={user}")

def user_tracks_from_lastweek(user, api_key):
    # Get the tracks from the last 7 days.
    today = date.today()
    lastWeekDate = datetime(today.year, today.month, today.day) - timedelta(days = 7)
    lastWeekDateTimeStamp = lastWeekDate.timestamp()

    return _request('user.getRecentTracks', api_key, params=f"&user={user}&from={lastWeekDateTimeStamp}")
