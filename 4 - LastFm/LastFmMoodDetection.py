# !/usr/bin/env python3

import argparse
import pathlib
import requests

from lastfm import lastfm_api

BASE_URL = "http://ws.audioscrobbler.com/2.0/?method="

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Analyses the mood of the given Last.Fm user based on their music consumption.')
parser.add_argument('user_id', type=str, help='The identifier of the user. Either their username or their identifier. Ex: Starkie785 - \'https://www.last.fm/user/Starkie785\'.')
parser.add_argument('-a', '--api_key', required=False, type=str, help='The API key for the application. If it is not provided, it will be read from the \'.secrets\' file.')

args = parser.parse_args()

user = args.user_id
api_key = args.api_key

# If no API key is provided, read it from the secrets store.
if not api_key:
    secrets = open('.secrets')
    api_key = secrets.read().strip()
    secrets.close()

# Check if the provided user exists.
print(f'Retrieving information from the user \'{user}\'')

userInfo = lastfm_api.user_info(user, api_key)

if 'error' in userInfo:
    print(f"{userInfo['message']} - {user}")
    exit()
