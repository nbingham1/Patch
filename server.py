#!/usr/bin/python

import http.server
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
 
server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
server_address = ("", 8000)
handler.cgi_directories = ["/cgi"]
 
httpd = server(server_address, handler)
httpd.serve_forever()
