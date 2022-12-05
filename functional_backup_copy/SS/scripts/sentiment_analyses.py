import pandas as pd
import numpy as np
from textblob import TextBlob
import feedparser
import requests
import json
import yaml
import re
from bs4 import BeautifulSoup
import spacy

## all in one:

def get_topic(txt): 
    headType = "text/raw"
    token = 'AisXlwqA1YPwYdneYj7CPZomubcPnjCr'
    url = "https://api-eit.refinitiv.com/permid/calais"
    payload = txt.encode('utf8')  ### THIS IS THE TEXT FORM THE NEWS WE WANT TO ACESS
    headers = {
        'Content-Type': headType,
        'X-AG-Access-Token': token,
        'outputformat': "application/json"
        }
    #  The daily limit is 5,000 requests, and the concurrent limit varies by API from 1-4 calls per second. 
    TRITResponse = requests.request("POST", url, data=payload, headers=headers)
    # Load content into JSON object
    JSONResponse = json.loads(TRITResponse.text)
    # print(json.dumps(JSONResponse, indent=4, sort_keys=True))


    #print('====Topics====')
    #print('Topics, Score')
    topics_dict={}
    i=0
    for key in JSONResponse:
        if ('_typeGroup' in JSONResponse[key]):
                if JSONResponse[key]['_typeGroup'] == 'topics':
                    #print(JSONResponse[key]['name'] + ", " + str(JSONResponse[key]['score']))
                    topics_dict[JSONResponse[key]['name']]=JSONResponse[key]['score']
            
    #print(topics_dict)

    topics= list(topics_dict)
    scores = list(topics_dict.values())
    if len(topics)>1:
        return "Topics||" + f"Topic: {topics[0]}, Score: {scores[0]}" 
    else:
        return ""


def get_sentiment(txt):
    headType = "text/raw"
    token = 'AisXlwqA1YPwYdneYj7CPZomubcPnjCr'
    url = "https://api-eit.refinitiv.com/permid/calais"
    payload = txt.encode('utf8')  ### THIS IS THE TEXT FORM THE NEWS WE WANT TO ACESS
    headers = {
        'Content-Type': headType,
        'X-AG-Access-Token': token,
        'outputformat': "application/json"
        }
    #  The daily limit is 5,000 requests, and the concurrent limit varies by API from 1-4 calls per second. 
    TRITResponse = requests.request("POST", url, data=payload, headers=headers)
    # Load content into JSON object
    JSONResponse = json.loads(TRITResponse.text)
    # print(json.dumps(JSONResponse, indent=4, sort_keys=True))

    #clean text
    clean_txt = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_txt) 
    # set sentiment 

    #print('\n====Sentiment====')

    if analysis.sentiment.polarity > 0: 
        return 'Sentiment|| Sentiment of the news: positive'
    elif analysis.sentiment.polarity == 0: 
        return 'Sentiment|| Sentiment of the news: neutral'
    else: 
        return'Sentiment|| Sentiment of the news: negative'
    
