#!/usr/bin/env python

"""
PUT extension to python server

curl or wget etc. to PUT files to server

curl -X PUT --upload-file somefile.txt http://localhost:8000
wget -O- --method=PUT --body-file=somefile.txt http://localhost:8000/somefile.txt
"""

import os
import sys
import http.server as server
import socketserver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port to use, default 9000")
args = parser.parse_args()

if args.port:
	PORT=int(args.port)
else:
	PORT=9000

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def do_PUT(self):
    	print(self.headers)
    	length = int(self.headers["Content-Length"])
    	path = self.translate_path(self.path)
    	with open(path, "wb") as dst:
    		dst.write(self.rfile.read(length))
    		
if __name__ == '__main__':
	with socketserver.TCPServer(("", PORT), HTTPRequestHandler) as httpd:
		print("example: curl -X PUT -T <file> ip:port")
		print("serving port", PORT)
		httpd.serve_forever()
