# !/usr/bin/env python3

import csv
import os
import pathlib
import string

# Load the AFINN file.
def _load_afinn():
    afinn_path = os.path.join(os.path.dirname(__file__), 'AFINN-111.txt')

    afinn = dict()

    with open(afinn_path, 'r') as afinn_file:
        reader = csv.reader(afinn_file, delimiter='\t')

        for row in reader:
            afinn[row[0]] = int(row[1])

    return afinn


afinn = _load_afinn()

# Analyse the sentiment of a given text.
def analyse_sentiment(text):
    clean_text = _remove_punctuation(text)

    sentiment = 0

    for word in clean_text.split():
        lowerWord = word.lower()
        sentiment += afinn.get(lowerWord, 0)

    return sentiment

# Remove the punctuation from the given string.
def _remove_punctuation(content):
    res = content

    for char in '“”' + string.punctuation:
        res = res.replace(char, "")

    return res
