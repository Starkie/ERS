# !/usr/bin/env python3

# Get the videos uploaded by a given user in Vimeo.

import requests
import argparse

baseUrl = 'https://vimeo.com/api/v2/'

def get_user_videos(user_id):
    return requests.get(baseUrl + f'{user_id}/videos.json').json()

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Get the videos from the given user Vimeo user.')
parser.add_argument('user_id', type=str, help='The identifier of the Vimeo user.')

args = parser.parse_args()

# Get the videos and print their titles.
videos = get_user_videos(args.user_id)

for v in videos:
    print(v['title'])