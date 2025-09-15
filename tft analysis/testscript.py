import tft_utils as tft
import re
import json
import requests
from apikey import apiheader

'''
TftDataUrl = "https://raw.communitydragon.org/latest/cdragon/tft/en_us.json"
TftRequestData = requests.get(TftDataUrl)
TftData = TftRequestData.json()
Setdata = TftData['setData']
ItemData = TftData['items']

itemComps = [item for item in ItemData if item['composition'] !=[]]
nonComp = [item for item in ItemData if item['composition']==[]]
'''
c,g,m = tft.get_highlevel_players(tft.Region.North_America.value)
c_results = json.loads(requests.get(c,headers=apiheader).text)
