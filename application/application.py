from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, Forbidden, NotAcceptable
from werkzeug.middleware.shared_data import SharedDataMiddleware

import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

from .utils import url_map

from .utils import Identity, render_template
from . import views

class Application(object):
    def __init__(self, config=None):
        
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True
        )
    def _dispatch_request(self,request):
        adapter = url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
            return response
        except NotFound:
            return render_template('404.html')
        except HTTPException as e:
            return e    
    def dispatch_request(self,request):
        identity = Identity(request)
        request.identity = identity
        return self._dispatch_request(request)
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(with_static=True):
    app = Application()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(
            app.wsgi_app, {"/static": os.path.join(os.path.dirname(__file__), "static")}
        )
    return app


