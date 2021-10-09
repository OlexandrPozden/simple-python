from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.wrappers import Response, Request
from werkzeug.exceptions import Forbidden

from jinja2 import Environment
from jinja2 import FileSystemLoader

from os import path

import jwt

from .models import User
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

def login_required(fun,**kwargs):
    def wrapper(request,**kwargs):
        if request.identity.logged_in:
            return fun(request,**kwargs)
        else:
            return render_template("login_required.html")
    return wrapper

def admin_required(fun,**kwargs):
    def wrapper(request):
        if request.identity.admin:
            return fun(request,**kwargs)
        else:
            return Forbidden("Only users with admin rights can access this page.")
    return wrapper

class AuthSettings:
    SECRET_KEY = 'k4Ndh1r6af5SZVnGitY82lpjK646apEnOAnc5lhW'
    USER_MODEL = User
    ALGORITHM = 'HS256'
    EXPIRATION_TIME = 300 ## in seconds
    TOKEN_NAME = 'token'

class JWTmanager(AuthSettings):
    def __init__(self, secret_key:str=None, algorithm:str=None, expiration_time:int=None):
        self.secret_key = self.SECRET_KEY if not secret_key else secret_key
        self.algorithm = self.ALGORITHM if not algorithm else algorithm
        self.expiration_time = self.EXPIRATION_TIME if not expiration_time else expiration_time
    def create_token(self,payload:dict)->str:
        if isinstance(payload,dict):
            payload['exp'] = datetime.datetime.utcnow()+datetime.timedelta(seconds=self.expiration_time)
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
        else:
            raise ValueError(f"Paylod should be instance of dict.")
    def get_payload(self,token):
        payload = {'error':0}
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            payload.update(decoded)
        except jwt.ExpiredSignatureError:
            payload["error"]="Token expired. Get new one"
        except jwt.InvalidTokenError:
            payload["error"]="Invalid Token"
        return payload
    def _create_payload(self, user)->dict:
        return {'sub':user.user_id,'username':user.username}

class Identity(AuthSettings):
    """Obtain request identity information
    
    From Request object it looks for cookie field 'token', decrypts it and
    inditificates client who send request."""

    def __init__(self, request:Request, secret_key:str=SECRET_KEY):
        self.username = ""
        self.user_id = ""
        self.logged_in = False
        self.admin = False

        self.token = request.cookies.get(self.TOKEN_NAME, None)

        self.jwtmanager = JWTmanager(self.SECRET_KEY if not secret_key else secret_key)

        if self.token:
            self._check_identity()
    def _get_payload(self):
        return self.jwtmanager.get_payload(self.token)
    def _check_identity(self):
        payload = self._get_payload()
        if not payload['error']:
            self.username = payload['username']
            self.user_id = payload['sub']
            self.logged_in = True
            self.admin = self._is_admin()
    def _is_admin(self):
        if self.user_id:
            user = self.USER_MODEL.get_by_id(self.user_id)
            return user.admin

class Auth(AuthSettings):
    jwtmanager = JWTmanager()
    @classmethod
    def login_user(cls, user, response:Response=None)->Response:
        """Logins User
        
        Pass User object."""
        if not response:
            response = Response()
        if isinstance(user,cls.USER_MODEL):
            payload = cls.jwtmanager._create_payload(user)
            token = cls.jwtmanager.create_token(payload)
            response.set_cookie(cls.TOKEN_NAME,token)
        else:
            raise ValueError(f"{user} is not instance of {cls.USER_MODEL}")
        return response
    @classmethod
    def logout_user(cls, user, response:Response=None)->Response:
        if not response:
            response = Response()
        response.delete_cookie(cls.TOKEN_NAME,None)
        return response
