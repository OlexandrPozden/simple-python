#!/usr/bin/env python

from urllib.parse import parse_qs
from html import escape
from views import home, signup, login, about

def application(environ, start_response):

    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        print(request_body_size)
    except (ValueError):
        request_body_size = 0

    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    # print(environ['wsgi.input'])
    # request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
    # print(request_body)
    # d = parse_qs(request_body)
    # print(d)
    # password1 = d.get('password', [''])[0] # Returns the first age value.
    # password2 = d.get('repeat-password', [''])[0] # Returns a list of hobbies.

    # # Always escape user input to avoid script injection
    # password1 = escape(password1)
    # password2 = escape(password2)

    # if password1 != password2:
    #     response_body="not equal"
    # response_body = "equal"
    
    if environ['PATH_INFO'] =='/':
        return home(environ, start_response)
    elif environ['PATH_INFO'] =='/signup':
        return signup(environ, start_response)
    elif environ['PATH_INFO'] =='/login':
        return login(environ, start_response)
    elif environ['PATH_INFO'] =='/about':
        return about(environ, start_response)    
    
    status = '200 OK'

    # response_headers = [
    #     ('Content-Type', 'text/html'),
    #     ('Content-Length', str(len(response_body)))
    # ]

    # start_response(status, response_headers)
    # return [response_body.encode()]
if __name__ == '__main__':    
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8000, application)
    httpd.serve_forever()