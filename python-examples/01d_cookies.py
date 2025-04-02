import requests

def print_cookies(cookiejar):
	for cookie in s.cookies:
		print(cookie)

s = requests.Session()
r = s.get('http://facebook.com')
print("Cookies after Facebook request\n=======")
print_cookies(s.cookies)

input()

r = s.get('http://google.com')
print("Cookies after Google request\n=========")
print_cookies(s.cookies)