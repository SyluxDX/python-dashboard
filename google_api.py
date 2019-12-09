""" google api data retreive """

import json
import requests
from pytrends.request import TrendReq

CHANNEL = 'hamaisemnos'
API_KEY = 'CHANGE THIS'
URL = 'https://www.googleapis.com/youtube/v3/channels?part={}&forUsername={}&key={}'

def get_youtube_data(part):
    """ get data from youtube api """
    aux = requests.get(URL.format(part, CHANNEL, API_KEY))
    return json.loads(aux.text)

def get_channel_logo():
    """ get chanel logo """
    # get image url
    jdata = get_youtube_data('snippet')
    image = jdata['items'][0]['snippet']['thumbnails']['default']['url']
    print(image)
    # get image
    with open('logo.png', 'wb') as imgfp:
        imgfp.write(requests.get(image).content)

def get_sub_count():
    """ get channel subscriber count """
    jdata = get_youtube_data('statistics')
    count = jdata['items'][0]['statistics']['subscriberCount']
    return count

def get_google_trends(region='portugal'):
    """ get top search """
    # get data
    data = TrendReq(tz=0).trending_searches(pn=region)
    # change column name
    data.columns = ['Top searchs in {}'.format(region.capitalize())]
    return data
