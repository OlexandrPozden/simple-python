from utils import render
from status_codes import error500
def home(environ, start_response):
    print("Home view")
    try:
        response_body = render("indhhhex.html")
        print("redered fine")
        start_response('200 OK',[('Content-Type','text/html'),('Content-length',str(len(response_body)))])
        return [response_body.encode()]

    except IOError as err:
        return error500(environ, start_response, str(err))
    