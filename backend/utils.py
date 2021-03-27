from .status_codes import error500

def render(environ, start_response,filename, code='200 OK', context={}):
    try:
        response_body = ""
        with open(filename, 'r') as f:
            response_body = f.read()
            response_body = response_body.format(**context)
        start_response(code,[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
        return [response_body.encode()]

    except IOError as err:
        return error500(environ, start_response, str(err))