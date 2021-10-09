from sqlalchemy.sql.functions import user
from werkzeug.wrappers import Request, Response
## REMOVE
#SECRET_KEY = 'k4Ndh1r6af5SZVnGitY82lpjK646apEnOAnc5lhW'

# @Request.application
# def application(request):
#     return Response(f"Hello {request.args.get('name', 'World!')}!")

# class BaseApplication(object):
#     def __init__(self): ...
#     def __call__(self, environ, start_response):
#         raise NotImplementedError

# class Dispatcher(BaseApplication):
#     def dispatch(environ, start_response):
#         pass

# class Application(Dispatcher):
#     def __init__(self):...
#     def __call__(self, environ, start_response):

from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from werkzeug.exceptions import HTTPException, NotFound, Forbidden, NotAcceptable
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

from .utils import url_map

from .utils import Auth, Identity
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
            return self.render_template('404.html')
        except HTTPException as e:
            return e    
    def dispatch_request(self,request):
        identity = Identity(request)
        request.identity = identity
        return self._dispatch_request(request)
    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype="text/html")
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


