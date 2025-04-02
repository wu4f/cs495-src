import requests
s = requests.Session()
loginurl = 'https://angr.oregonctf.org/'
loginpayload = {"username":"demo0", "passwd":"malware"}
resp = s.post(loginurl, data=loginpayload)
print(resp.text)