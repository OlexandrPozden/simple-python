import time

def error500(environ, start_response, info=""):
    info_response = "\n"+info
    start_response('500 Internal Server Error',[('Content-type','text/plain')])
    return [b'500 Internal Server Error', info_response.encode()]

def notfound(environ, start_response):
    code = '404 Not Found'
    filename = 'static/404.html'
    try:
        response_body = ""
        with open(filename, 'r') as f:
            response_body = f.read()
        start_response(code,[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
        return [response_body.encode()]

    except IOError as err:
        return error500(environ, start_response, str(err))


def ok200(environ, start_response):
    
    a = time.time()
    start_response('200 OK', [('Content-Type','text/plain')])
    
    b = time.time()
    print("200ok start_response: {:.5f}".format(b-a))
    return [b'200 OK']