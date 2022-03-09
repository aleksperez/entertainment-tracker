import requests as req
from dotenv import load_dotenv
import os

load_dotenv()
APIKEY= os.getenv('TMDB_API')

def nested_get(d, level1_key, level2_key, level3_key):
    elements = []
    try:
        return d[level1_key][level2_key][level3_key]
    except KeyError:
        return elements

def get_json(media,search):
    response = req.get(f"https://api.themoviedb.org/3/search/{media}?api_key={APIKEY}&query={search}")
    return None if response.status_code != 200 else response.json()

def get_overview(json):
    return json.get('overview') if json else None

def get_title(media,json):
    if media=='movie':
        return json.get('title') if json else None
    if media == 'tv':
        return json.get('name') if json else None

def get_id(json):
    return json.get('id') if json else None

def get_poster(json):
    path = json.get('poster_path')
    return 'https://image.tmdb.org/t/p/original/'+path if json else None

def get_providers(media,id):
    response = req.get(f"https://api.themoviedb.org/3/{media}/{id}/watch/providers?api_key={APIKEY}")
    json = response.json()
    providers=[] 
    if json:
        provs = nested_get(json,'results','US', 'flatrate')
        for i in range(len(provs)):
            providers.append(provs[i].get('provider_name'))
    return providers
