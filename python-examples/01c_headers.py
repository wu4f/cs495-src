import requests
s = requests.Session()
url = 'http://mercury.picoctf.net:1270/'
headers = {
  'User-Agent' : 'PicoBrowser',
  'Referer' : url,
  'Date' : 'Wed, 21 Oct 2018 00:00:00 GMT',
  'DNT' : 'true',
  'X-Forwarded-For' : '2.16.66.0',
  'Accept-Language' : 'sv'
}
resp = s.get(url, headers=headers)
print(resp.text)