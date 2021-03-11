
from .utils import render
from .status_codes import error500

def home(environ, start_response):
    return render(environ, start_response, 'static/home.html')

def signup(environ, start_response):
    return render(environ, start_response, 'static/signup.html')

def login(environ, start_response):
    if environ.get('REQUEST_METHOD').lower() == 'post':
        params = environ.get('params')
        if params['username'] == 'aska':
            return main(environ, start_response)
        else:
            return home(environ, start_response)
    return render(environ, start_response, 'static/login.html')

def main(environ, start_response):
    return render(environ, start_response, 'static/main.html')



def about(environ, start_response):
    return render(environ, start_response, 'static/about.html')       