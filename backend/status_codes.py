def error500(environ, start_response, info=""):
    info_response = "\n"+info
    start_response('500 Internal Server Error',[('Content-type','text/plain')])
    return [b'500 Internal Server Error', info_response.encode()]