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


class Application(object):
    def __init__(self, config=None):
        self.url_map = Map(
            [
                Rule("/", endpoint="index"),
                Rule("/login", endpoint="login"),
                Rule("/main", endpoint="main"),
            ]
        )
    @staticmethod
    def index(request):
        return Response([b"Index page"])
    @staticmethod
    def login(request):
        return Response([b'Here we to log in'])
    @staticmethod
    def main(request):
        return Response([b'MAIN'])
    def dispatch_request(self,request):
        endpoint_to_views={
            "index":self.index,
            "login":self.login,
            "main":self.main,
        }
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint_to_views[endpoint](request)
        except HTTPException as e:
            return e
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

application = Application()