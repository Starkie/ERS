# !/usr/bin/env python3

import json
import csv
import argparse

states_names = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC':'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
'SC': 'South Carolina', 'SD': 'South Dakota', 'TN':'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia',
'WA': 'Washington','WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}

states = [state.lower() for state in states_names.keys()]

def getState(data):
    if data["place"] != None and data["place"]["country_code"] == "US":
        state = str(data["place"]["full_name"]).lower().split(", ")
        if len(state) > 1:
            return state[1]

def isState(state):
    if state in states:
        return True
    return False 

def readTweets():
    file = "output.txt"

    array = []
    with open(file, "r") as ins:

        for line in ins:          
         if ( len(line)> 1): ## to avoid empty lines 
           data = json.loads(line)
           if "created_at" in data:
               state = getState(data)
               if isState(state):
                 if "text" in data:
                    print (data["text"])
                    print (state)

# Declare the script parameters.
parser = argparse.ArgumentParser(description='Analyses the sentiment on a given country from a collection of tweets.')
parser.add_argument('file', type=str, help='Path to the file containing the tweets encoded in the JSON format.')

args = parser.parse_args()