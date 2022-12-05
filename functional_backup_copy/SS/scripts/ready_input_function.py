import requests
from bs4 import BeautifulSoup
import re
import spacy
import pandas as pd


def get_page_clean_text(url):
    html_page = requests.get(url).content
    soup = BeautifulSoup(html_page)
   
    whitelist = ['p', 'strong', 'em', 'b', 'u', 'i', 'h1', 'h2', 'h3']
    out = ""

    for t in soup.find_all(text=True):
        if t.parent.name in whitelist:
            out += '{} '.format(t)
    
    escape = ['\r', '\n', '\t', '\xa0']        
        
    for e in escape:
        out = out.replace(e, '')

    clean_text= out.replace('!', ' exclamation ')
    clean_text = clean_text.replace('?', ' question ')
    #news[column] = news[column].replace('\'', ' quotation ')
    clean_text = clean_text.replace('\"', ' quotation ')
    clean_text = clean_text.lower().strip()
    
    return clean_text