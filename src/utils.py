import os
import json
import html
import unicodedata
import requests
import re

from random import random, randrange

from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import Popularity



def get_website(page_link : str, random_user_agent : bool = True):
    """
    Obtains and parses the html from given page. 
    
    params:
    page_link (str): link to page to obtain the html from 
    random_user_agent (bool): If set to True then user agent is shuffled and
    randomly selected based on the popularity of given user agent.
    
    returns:
    soup (BeautifulSoup): bs4 object containing obtained html.
    
    """
    if random_user_agent:
        user_agent_rotator = UserAgent(popularity = [Popularity.COMMON.value,
                                                     Popularity.POPULAR.value],
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        headers = {'User-Agent' : user_agent}
    else:
        headers = None
    try:
        response = requests.get(page_link, headers=headers)
        content = response.content.decode('utf-8')
        content = html.unescape(content)
        content = unicodedata.normalize("NFKD", content)
        soup = BeautifulSoup(content, 'html.parser')
    except:
        print('Error occured')
        soup = None
    return soup



def find_metadata_json(soup):
    """
    Extracts json file from main tvp page contaning articles metadata.
    
    params:
    soup (BeautifulSoup): bs4 object containing obtained html.
    
    returns:
    items (dict): dictionary containg metadata of articles present on given page.
    dictionary contains three fields: url, title and lead.
    """
    script = soup.find('script', string=re.compile('window.__directoryData'))
    json_text = re.search(r'^\s*window.__directoryData\s*=\s*({.*?})\s*;\s*$',
                        script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    items = data['items']
    
    return items



def obtain_info(page_link : str, domain : str, page : int):
    """
    Obtains all links, titles and leads of articles present on given page.
    
    params:
    page_link (str): formatable string
    domain (str): string representing section on tvp.info
    page (int): number of page to obtain metadata from
    
    returns:
    tuple: containing links, titles and lead of articles present on given page.
    """
    page_link = page_link.format(domain = domain, page = page)
    
    print(f'stealing from: {page_link}')
    
    soup = get_website(page_link=page_link)
    json_metadata = find_metadata_json(soup=soup)
    
    page_links = ['https://www.tvp.info' + x['url'] for x in json_metadata]
    page_leads = [ x['lead'] for x in json_metadata]
    page_titles = [ x['title'] for x in json_metadata]
    
    return page_links, page_leads, page_titles



def get_content(link : str, title : str, headline : str):
    """
    Obtains full article.
    
    params:
    link (str): link to the article
    title (str): title of the article
    headline (str): lead of the article
    
    returns:
    dict: containg all info about article
    """
    
    soup = get_website(link)
    text_parts = soup.find_all('p', {'class' : "am-article__text article__width"})
    full_content = ' '.join([bit.get_text() for bit in text_parts])
    
    return {'link' : link,
            'title' : title,
            'headline' : headline,
            'content' : full_content}


