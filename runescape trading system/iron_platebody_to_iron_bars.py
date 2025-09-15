import requests
import json
api_endpoint = "https://api.weirdgloop.org/exchange/history/osrs/all?id=314"
mappings = "http://prices.runescape.wiki/api/v1/osrs/mappings"
header_update = {
    'User-Agent':'RuneScape optimal price finder for iron bars-Imhotep#0019',
    'from' : 'shakarunemaster@gmail.com'
    }
#item_mapping_request = requests.get(mappings,headers=header_update)
feathers = json.loads(requests.get(api_endpoint,headers=header_update).text)

