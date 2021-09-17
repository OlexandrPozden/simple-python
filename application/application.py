from sqlalchemy.sql.functions import user
from werkzeug.wrappers import Request, Response

SECRET_KEY = 'k4Ndh1r6af5SZVnGitY82lpjK646apEnOAnc5lhW'

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
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey  

import datetime
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

import jwt

base = declarative_base()
class Post(base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="DELETE"))
    published = Column(Boolean, default=False, nullable=False)
    request_publish = Column(Boolean, default=False, nullable=False)
    published_time = Column(DateTime)
    created_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    def __repr__(self):
        return '<Post %r>' % self.post_id

class User(base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    def __repr__(self):
        if self.admin:
            return '<Admin %r>' % self.username
        return '<User %r>' % self.username

def admin_required(fun):
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.identity:
            if self.identity.admin:
                return fun(*args, **kwargs)
        return redirect('/main')
    return wrapper
def login_required(fun): 
    def wrapper(*args, **kwargs):
        self = args[0]
        request = args[1]
        if self.identity:
            return fun(*args, **kwargs)
        else:
            self.turn_back_to = request.path
            return redirect('/login')
    return wrapper
def create_token(payload):
    payload['exp'] = datetime.datetime.utcnow()+datetime.timedelta(seconds=300)
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def payload_from_token(token):
    payload = {}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print("Token is still valid and active")
    except jwt.ExpiredSignatureError:
        print("Token expired. Get new one")
    except jwt.InvalidTokenError:
        print("Invalid Token")
    return payload

class Application(object):
    def __init__(self, config=None):
        engine = create_engine('sqlite:///test.db', echo=False)
        Session = sessionmaker(engine)  
        self.session = Session()
        base.metadata.create_all(engine)

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
                Rule('/admin', endpoint="admin"),
                Rule('/logout', endpoint="logout"),
                Rule('/post', endpoint="main"),
                Rule('/post/<int:post_id>', endpoint="post"),
                Rule('/post/<int:post_id>/edit', endpoint="post/edit"),
                Rule('/post/new', endpoint="post/new"),
                Rule('/post/<string:authorname>', endpoint="post/authorname"),
            ]
        )
        self.turn_back_to = "" ## turn back to page where user was redirected from
        
        self.identity = None ## <class 'User'> if logged in

    ## custom functions
    @property
    def path_to_turn_back(self):
        if self.turn_back_to:
            path = self.turn_back_to
            self.turn_back_to = ""
            return path
        return self.turn_back_to
    def login_user(self, user, redirect_to=None):
        token = create_token(self._create_payload_from_user(user))
        response = redirect(self.path_to_turn_back or redirect_to or '/main')
        response.set_cookie("token",token)
        return response
    def logout_user(self, response:Response)->Response:
        if self.identity:
            self.identity = None
            response.delete_cookie("token")
        return response
    def _create_payload_from_user(self, user:User)->dict:
        return {'sub':user.user_id,'username':user.username}
    def _identity_check(self, request):
        token = request.cookies.get('token', None)
        if token:
            payload = payload_from_token(token)
            if payload:
                user_id = payload.get('sub','')
                username = payload.get('username','')
                user = self.get_user_by_id(user_id)
                if user:
                    if user.username == username:
                        self.identity = user


    ## views     
    def index(self,request):
        return self.render_template('index.html')
    def login(self,request):
        error=""
        if request.method == 'POST':
            username = request.form.get('username','')
            password = request.form.get('password','')

            user = self.get_user_by_name(username)
            if not user or not check_password_hash(user.password, password): 
                error = "Wrong credentials."
                return self.render_template('login.html', error=error)
            else:
                ## return token and render template
                response = self.login_user(user)
                return response
        return self.render_template('login.html', error=error)
    def logout(self,request):
        return self.logout_user(redirect('/'))
    @admin_required
    def admin(self,request):
        return Response('Admin page')
    def main(self,request):
        error = ""
        username = None
        posts = self.read_posts()

        if self.identity:
            username = self.identity.username
        return self.render_template('main.html', posts=posts, error=error, username=username)
    
    def signup(self,request):
        error = ''
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            ## check if user already exist
            ## if not register new one
            user = self.session.query(User).filter_by(username=username).first()
            if user:
                ## need some flash to show this
                error = "User already registered. Please, use another username."
                return self.render_template('signup.html', error=error)
            else:
                new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
                self.add_user(new_user)
                response = self.login_user(new_user) ## method login_user already returns response
                return response
        return self.render_template('signup.html')
    @login_required
    def post_new(self, request):
        if request.method == 'POST':
            title = request.form.get('title')
            text = request.form.get('text')
            request_publish = bool(request.form.get('request_publish'))
            user_id = self.identity.user_id

            post = Post(title=title, text=text, request_publish = request_publish, user_id=user_id)
            self.post_post(post)

        return self.render_template('new_post.html',post=None)
    @login_required
    def post_edit(self, request, post_id):
        post = self.get_post(post_id)
        if post:
            ## is author of that post
            if post.user_id == self.identity.user_id: 
                return self.render_template('new_post.html', post=post)
        return self.render_template('404.html')
    @login_required
    def post(self, request, post_id):
        post = self.read_post(post_id)
        if post: 
            return self.render_template('post.html', post=post)
        return self.render_template('404.html')
    @login_required
    def users_posts(self, request, authorname):
        print(authorname)
        is_owner = False
        author = self.get_user_by_name(authorname)
        ## select all posts from that author
        posts = self.get_posts_by_user_id(author.user_id)
        if self.identity.user_id == author.user_id:
            is_owner = True
        return self.render_template('users_posts.html', posts=posts, is_owner=is_owner)
    ## database calls
    def create_admin(self,username:str, password:str)->None:
        ## hash password
        password = generate_password_hash(password, method='sha256') 
        print('Creating <admin %r>...'%username)
        admin = User(username=username, password=password, admin=True)
        self.add_user(admin)
    def get_user_by_id(self, id):
        return self.session.query(User).filter_by(user_id=id).first()
    def get_user_by_name(self, name):
        return self.session.query(User).filter_by(username=name).first()
    def add_user(self, user:User)-> None:
        self.session.add(user)
        self.session.commit()
    def get_post(self, post_id):
        post = self.session.query(Post).filter_by(post_id==post_id).first()
        return post
    def post_post(self,post:Post)->None:
        self.session.add(post)
        self.session.commit()
    def read_posts(self):
        posts = self.session.query(Post)
        return [p for p in posts]
    def get_posts_by_user_id(self, user_id):
        posts = self.session.query(Post).filter(Post.user_id == user_id).all()
        print("author posts:",posts)
        return [p for p in posts]
    def update_post(self, post:Post): ## deprecated
        post_id = post.post_id
        try:
            old_post = self.session.query(Post).filter_by(post_id=post_id).first()
            old_post = post
            self.session.commit()
        except:
            print("Post with post id: %s does not exist" % post_id)
    def delete_post(self, post_id):
        self.session.query(Post).filter_by(post_id=post_id).delete()
        self.session.commit()


    ## additional server functionality
    def _dispatch_request(self,request):
        endpoint_to_views={
            "index":self.index,
            "login":self.login,
            "main":self.main,
            "signup":self.signup,
            "admin":self.admin,
            "logout":self.logout,
            "post/new":self.post_new,
            "post/edit":self.post_edit,
            "post": self.post,
            "post/authorname":self.users_posts,
        }
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint_to_views[endpoint](request,**values)
        except NotFound:
            return self.render_template('404.html')
        except HTTPException as e:
            return e    
    def dispatch_request(self,request):
        self._identity_check(request)
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