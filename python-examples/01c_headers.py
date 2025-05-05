import requests
s = requests.Session()
url = 'http://mercury.picoctf.net:1270/'
req_headers = {
  'User-Agent' : 'PicoBrowser',
  'Referer' : url,
  'Date' : 'Wed, 21 Oct 2018 00:00:00 GMT',
  'DNT' : 'true',
  'X-Forwarded-For' : '2.16.66.0',
  'Accept-Language' : 'sv'
}
resp = s.get(url, headers=req_headers)
print(resp.text)
