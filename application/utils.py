from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.wrappers import Response

from jinja2 import Environment
from jinja2 import FileSystemLoader

from os import path

url_map = Map()

TEMPLATE_PATH = path.join(path.dirname(__file__), "templates")
STATIC_PATH = path.join(path.dirname(__file__), "static")

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
