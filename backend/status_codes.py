def error500(environ, start_response, info=""):
    info_response = "\n"+info
    start_response('500 Internal Server Error',[('Content-type','text/plain')])
    return [b'500 Internal Server Error', info_response.encode()]

def notfound(environ, start_response):
    start_response('404 Not Found', [('Content-Type','text/plain')])
    return [b'404 Not Found']


def ok200(environ, start_response):
    start_response('200 OK', [('Content-Type','text/plain')])
    return [b'200 OK']