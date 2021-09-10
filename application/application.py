from werkzeug.wrappers import Request, Response

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
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import redirect
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

class Application(object):
    def __init__(self, config=None):
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True
        )
        self.url_map = Map(
            [
                Rule("/", endpoint="index"),
                Rule("/login", endpoint="login"),
                Rule("/main", endpoint="main"),
                Rule('/signup', endpoint="signup"),
            ]
        )
    def index(self,request):
        return self.render_template('index.html')
    def login(self,request):
        return self.render_template('login.html')
    def main(self,request):
        return self.render_template('main.html')
    def signup(self,request):
        return self.render_template('signup.html')
    def dispatch_request(self,request):
        endpoint_to_views={
            "index":self.index,
            "login":self.login,
            "main":self.main,
            "signup":self.signup,
        }
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint_to_views[endpoint](request)
        except HTTPException as e:
            return e
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
application = create_app()