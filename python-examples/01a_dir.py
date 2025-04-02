import requests
r = requests.get('http://thefengs.com')
print(type(r))
print(dir(r))