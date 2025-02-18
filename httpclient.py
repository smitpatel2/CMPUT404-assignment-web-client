#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re

# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        # Use urllib.parse.urlparse to extract the host and port from the URL
        url = urllib.parse.urlparse(url)
        port = url.port
        # If the port is not specified, use the default HTTP port (80)

        if port is None:
            port = 80
        
        host = url.hostname

        return host, port
    def get_path(self, url):
        # Use urllib.parse.urlparse to extract the path from the URL

        url = urllib.parse.urlparse(url)
        path = url.path
        if not path:
            return "/"
        return path

    def connect(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        return None

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        status_code = int(data.split()[1])

        return None

    def get_headers(self,data):
        header = data.split('\r\n\r\n')[0]

        return None

    def get_body(self, data):
        body = data.split('\r\n\r\n')[1]

        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        # Extract the host and port from the URL

        host, port = self.get_host_port(url)
        # Extract the path from the URL

        path = self.get_path(url)

        # connecting
        try:
            self.connect(host, port)
        except:
            return HTTPResponse(404)
        
        result_url = f'GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'
        self.sendall(result_url)

        received_data = (self.recvall(self.socket))
        # Extract the HTTP status code and response body from the received data using the get_code and get_body functions

        code = self.get_code(received_data)
        body = self.get_body(received_data)
        
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        host, port = self.get_host_port(url)
        path = self.extract_path(url)
            
        # connecting
        try:
            self.connect(host, port)
        except:
            return HTTPResponse(404)

        # If args is None, set it to an empty string
        if not args:
            args = "" 
        else:
            args = urllib.parse.urlencode(args)
        # Construct the POST request string to be sent
        result_url = f'POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {(len(args))}\r\nConnection: close\r\n\r\n{args}'
        self.sendall(result_url)

        received_data = (self.recvall(self.socket))
        # Extract the HTTP status code and response body from the received data using the get_code and get_body functions
        code = self.get_code(received_data)
        body = self.get_body(received_data)
        
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
