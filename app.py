#!/usr/bin/env python

from urllib.parse import parse_qs
from html import escape
from backend.views import home, signup, login, about

def application(environ, start_response):

    if environ['PATH_INFO'].lower() =='/':
        print("path home")
        return home(environ, start_response)
    elif environ['PATH_INFO'].lower() =='/signup':
        print("path signup")
        return signup(environ, start_response)
    elif environ['PATH_INFO'].lower() =='/login':
        return login(environ, start_response)
    elif environ['PATH_INFO'].lower() =='/about':
        return about(environ, start_response)    
    else:
        response_body = b"it works with python proxy"
        start_response('200 OK',[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
        return [response_body]
    

class Application():
    def __init__(self,s):
        pass
if __name__ == '__main__':    
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 7000, application)
    httpd.serve_forever()