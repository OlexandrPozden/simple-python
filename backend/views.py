__name__ ="views"

from .utils import render
from .status_codes import error500

def home(environ, start_response):
    print("Home view")
    try:
        response_body = render("static/index.html")
        print("redered fine")
        start_response('200 OK',[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
        return [response_body.encode()]

    except IOError as err:
        return error500(environ, start_response, str(err))

def signup(environ, start_response):
    try:
        response_body = render("static/signup.html")
        print("redered fine")
        start_response('200 OK',[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
        return [response_body.encode()]

    except IOError as err:
        return error500(environ, start_response, str(err))

def login(environ, start_response):
    read_elements = int(environ.get('CONTENT_LENGTH', 0))
    response_body = environ['wsgi.input'].read(read_elements)
    
    start_response('200 OK',[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
    return [response_body]

def about(environ, start_response):
    read_elements = int(environ.get('CONTENT_LENGTH', 0))
    response_body = environ['wsgi.input'].read(read_elements)
    
    start_response('200 OK',[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
    return [response_body]        