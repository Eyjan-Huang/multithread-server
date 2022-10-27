"""
This file stores all the configuration variables for globally used
"""
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Socket info
HOST = '127.0.0.1'
PORT = 9999
IP = AF_INET
PROTOCOL = SOCK_STREAM
SOCK_LEVEL = SOL_SOCKET
RULE = SO_REUSEADDR


# File path info
ROOT_PATH = './file'


# HTTP response info
OK = '''HTTP/1.1 200 OK\r
Date: {d}\r
Connection: keep-alive\r
Content-Length: {cl}\r
Content-Type: {ct}\r
\r
'''

BAD_REQUEST = '''HTTP/1.1 400 Bad Request\r
Date: {d}\r
Connection: keep-alive\r
Content-Length: None\r
Content-Type: None\r
\r

ERROR 400: Request Error
It seems like your request is invalid format or content is too large
'''

FORBIDDEN = '''HTTP/1.1 403 Forbidden\r
Date: {d}\r
Connection: keep-alive\r
Content-Length: None\r
Content-Type: None\r
\r

ERROR 403: Forbidden Access
Sorry, you do not have the privilege to access the corresponding content
'''

NOT_FOUND = '''HTTP/1.1 404 Not Found\r
Date: {d}\r
Connection: keep-alive\r
Content-Length: None\r
Content-Type: {ct}\r
\r

ERROR 404: Page Not Found
Sorry...The file you are looking for is not found in the server
'''
