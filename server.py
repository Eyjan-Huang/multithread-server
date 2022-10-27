"""
COEN317 Distributed System - Programming Assignment 1
Yingjian Huang
W1609532

This project generates a simple web server which allows the user to do some HTTP interaction in between.
According to the requests, the server will either display the target or error messages in browser.

In brief, it mainly supports the following responses:
200 - OK
400 - Bad Request
403 - Permission Denied
404 - Not Found
"""

import socket
import time

from threading import Thread
from datetime import datetime
from config.server_config import *


def get_localtime():
    """
    Return the localtime using the given format

    :return: formatted time in String
    """
    time_format = '%a, %d %b %Y %H:%M:%S PST'
    pst = datetime.now()
    return pst.strftime(time_format)


def get_resources(path, ct):
    """
    Get the target resources based on the path given

    :param path: the file path
    :param ct: content-type placeholder
    :return: the resources in binary format
    """
    with open(path, 'rb') as f:
        content = f.read()
        header = OK.format(d=get_localtime(), cl=len(content), ct=ct).encode()
        response = header + content
        print(header.decode())
    return response


def get_content_type(uri):
    """
    Return the corresponding content type

    :param uri: the target URI
    :return: content-type
    """
    suffix = uri if uri == '/' else uri.split('.')[-1]
    memo = {
        'html': 'text/html',
        'jpg': 'image/jpg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'txt': 'text/plain'
    }
    return memo[suffix] if suffix in memo else None


def get_target(header):
    """
    Get the request method and URI of the request

    :param header: the HTTP request header
    :return: (method, URI)
    """
    buffer = header.split(' ')

    if len(buffer) < 2:
        return None, '/exit'

    method, uri = buffer[0], buffer[1]
    uri = uri if uri != '/' else '/index.html'
    return method, uri


def handle_request(conn):
    """
    Handle the requests from the users

    :param conn: the connection
    :return: None
    """
    global running
    request = conn.recv(1024).decode()
    method, uri = get_target(request)
    content_type = get_content_type(uri)

    # print(request, method, uri, sep='\n')     # If you want to see the log, uncomment this line

    if uri == '/exit':
        running = False     # Terminate the server
        return None
    elif len(uri.split('%%')) > 1:
        response = BAD_REQUEST.format(d=get_localtime()).encode()   # Send HTTP 400
        print(response.decode())
    elif uri == '/sudo':
        response = FORBIDDEN.format(d=get_localtime()).encode()     # Send HTTP 403
        print(response.decode())
    else:
        path = ROOT_PATH + uri
        try:
            response = get_resources(path, content_type)    # Send HTTP 200
        except FileNotFoundError:
            response = NOT_FOUND.format(d=get_localtime(), ct=content_type).encode()    # Send HTTP 404
            print(response.decode())
    conn.sendall(response)
    conn.settimeout(900)    # If after 900 secs there is no request comes in, auto terminate server


def init():
    """
    Initialize the server and send the response based on what users gave

    :return: None
    """
    global running
    s = socket.socket(IP, PROTOCOL)     # (IPv4, TCP)
    s.setsockopt(SOCK_LEVEL, RULE, 1)   # Tell the server we allow reuse the port number for testing
    s.bind((HOST, PORT))
    s.listen(3)     # Maximum 3 waiting connections

    while running:
        conn, addr = s.accept()
        thread = Thread(target=handle_request, args=(conn,))    # When request comes in, generate a new thread to handle
        thread.setDaemon(True)      # Set as deamon, in case of unexpected running after main thread terminates
        thread.start()

        if not running:
            time.sleep(1)   # To safely terminate the server, sleep for 1 sec then block the current thread
            thread.join()
            break
    conn.close()
    s.close()


if __name__ == '__main__':
    running = True  # This is a global variable that controls whether to terminate the server
    init()
