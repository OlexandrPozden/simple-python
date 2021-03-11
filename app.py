#!/usr/bin/env python

from urllib.parse import parse_qs
from html import escape
from backend.views import home, signup, login, about, main
from backend.url import urlpatterns
from backend.status_codes import notfound
import cgi
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
    elif environ['PATH_INFO'].lower() =='/main':
        return main(environ, start_response)    
    else:
        response_body = b"it works with python proxy"
        start_response('200 OK',[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
        return [response_body]
    

class Application():
    def __init__(self):
        pass
    def __call__(self, environ, start_response):
        method = environ.get('REQUEST_METHOD').lower()
        path = environ.get('PATH_INFO')
        params = cgi.FieldStorage(environ.get('wsgi.input'), environ=environ)
        environ['params'] = {k:params.getvalue(k) for k in params}
        handler = urlpatterns.get((method,path), notfound)
        return handler(environ, start_response)
if __name__ == '__main__':    
    from wsgiref.simple_server import make_server
    app = Application()
    httpd = make_server('localhost', 7000, app)
    httpd.serve_forever()