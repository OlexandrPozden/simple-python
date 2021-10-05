from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.wrappers import Response
from werkzeug.exceptions import Forbidden

from jinja2 import Environment
from jinja2 import FileSystemLoader

from os import path

url_map = Map()

TEMPLATE_PATH = path.join(path.dirname(__file__), "templates")
SECRET_KEY = 'k4Ndh1r6af5SZVnGitY82lpjK646apEnOAnc5lhW'

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

def expose(rule,**kw):
    def decorate(f):
        kw["endpoint"] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f

    return decorate

def render_template(template, **context):
    return Response(
        jinja_env.get_template(template).render(**context), mimetype="text/html"
    )

def login_required(fun):
    def wrapper(request):
        if request.identity.logged_in:
            return fun(request)
        else:
            return render_template("login_required.html")
    return wrapper

def admin_required(fun):
    def wrapper(request):
        if request.identity.admin:
            return fun(request)
        else:
            return Forbidden("Only users with admin rights can access this page.")
