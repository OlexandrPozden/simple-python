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
from werkzeug.exceptions import HTTPException, NotFound, Forbidden, NotAcceptable
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey  

import datetime
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

import jwt

base = declarative_base()

engine = create_engine('sqlite:///test.db', echo=False)
Session = sessionmaker(engine)  
session = Session()
base.metadata.create_all(engine)

class DbManipulation:
    @classmethod
    def get_all(cls):
        return session.query(cls).all()
    @classmethod
    def save(cls,obj):
        if isinstance(obj,cls):
            session.add(obj)
            session.commit()
        else:
            raise Exception("Wrong object type")  
    @classmethod
    def get_by_id(cls,id):
        return session.query(cls).filter(getattr(cls,cls.__name__+"id") == id).first()
    @classmethod
    def get_by_field(cls,**field):
        """
        Pass only one argument!
        User.get_by_field(username="Bob")
        Post.get_by_field(title="my first post")
        User.get_by_field(admin=True)
        """
        if len(field) == 1:
            field_name, value  = list(field.items())[0]
            if hasattr(cls, field_name):
                return session.query(cls).filter(getattr(cls, field) == value).all()
            else:
                raise ValueError(f"Field {field_name} does not exist in context of {cls.__name__} model.")
        else:
            raise ValueError(f"Expected lenght of fields 1, but got {len(field)}")
    @classmethod
    def delete_by_id(cls,id):
        session.query(cls).filter(getattr(cls,cls.__name__+"id") == id).delete()
        session.commit()
    @classmethod
    def delete(cls,obj):
        if isinstance(obj,cls):
            cls.delete_by_id(obj,getattr(cls,cls.__name__+"id"))
        else:
            raise Exception("Wrong object type")
  
class User(base,DbManipulation):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        if self.admin:
            return '<Admin username\'%r\'>' % self.username
        return '<User username=\'%r\'>' % self.username

class Post(base,DbManipulation):
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
    
    @classmethod
    def full_details(cls, **filter):
        """Returns details about post with the given filter

        This method implemented only for Post model.
        So when we call this method, we get the full details of
        that post and in addition we get the author of that post,
        with its unique user_id

        Parameters
        ----------
        filter : dict
            Statements which used to filter the query, where key is a field
            of the model.

        Returns
        -------
        list
            List of tuples, where tuple is united object of two models (Post,User).
        
        Examples
        --------
        >>>Post.full_details(published=True)
        ...

        """
        all_posts = session.query(Post.post_id,
                            Post.title,
                            Post.text,
                            Post.published_time,
                            Post.published, 
                            User.user_id,
                            User.username).join(User)
        ## filter the response
        for attr, value in filter.items():
            all_posts = all_posts.filter(getattr(Post, attr)==value)
        return all_posts.all()
        
    def __repr__(self):
        return '<Post post=id=\'%r\'>' % self.post_id


def admin_required(fun):
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.identity:
            if self.identity.admin:
                return fun(*args, **kwargs)
        return Forbidden('Only users with admin permission can reach this page.')
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
        self.session = session
        
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
                Rule('/about', endpoint="about"),
                Rule('/post', endpoint="main"),
                Rule('/post/<int:post_id>', endpoint="post"),
                Rule('/post/<int:post_id>/edit', endpoint="post/edit"),
                Rule('/post/new', endpoint="post/new"),
                Rule('/post/<string:authorname>', endpoint="post/authorname"),
                Rule('/post/<int:post_id>/request_publish', endpoint="post/request_publish"),
                Rule('/post/<int:post_id>/publish', endpoint="post/publish"),
                Rule('/post/<int:post_id>/delete', endpoint="post/delete"),
                Rule('/authors', endpoint="authors")
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
    def about(self,request):
        return self.render_template('about.html')
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
        posts = self.get_requested_posts()
        return self.render_template('admin.html',posts=posts)
    def main(self,request):
        posts = self.get_all_public_posts()
        error = ""
        username = None
        # posts = self.read_posts()

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
            username = self.identity.username

            post = Post(title=title, text=text, request_publish = request_publish, user_id=user_id)
            self.post_post(post)

            return redirect('/post/%s'%username)

        return self.render_template('new_post.html',post=None)
    @login_required
    def post_edit(self, request, post_id):
        if request.method == 'POST':
            request_publish = bool(request.form.get('request_publish'))
            title = request.form.get('title')
            text = request.form.get('text')
            self.update_post_by_fields(post_id,
            title=title,
            text=text,
            request_publish=request_publish,
            published=False,
            updated_time = datetime.datetime.utcnow()
            )
            return redirect('/post/%s'%self.identity.username)
            #return self.render_template('post.html', post=post)
        post = self.get_post(post_id)
        if post:
            ## is author of that post
            if post.user_id == self.identity.user_id: 
                return self.render_template('new_post.html', post=post)
        return self.render_template('404.html')
    @login_required
    def post(self, request, post_id):
        is_owner = False
        is_admin = False
        post = self.get_post(post_id)
        if post: 
            if self.identity.user_id == post.user_id: 
                is_owner = True
            is_admin = self.identity.admin
            return self.render_template('post.html', post=post,is_owner=is_owner, is_admin=is_admin)
        return self.render_template('404.html')
    @admin_required
    def post_publish(self, request, post_id):
        post = self.get_post(post_id)
        if not post: 
            return NotFound
        else:
            if not post.request_publish:
                return redirect('/admin') 
            self.update_post_by_fields(post_id, request_publish=False, published=True, published_time=datetime.datetime.utcnow())
            return redirect('/admin')
    @login_required
    def request_publish(self, request, post_id):
        post = self.get_post(post_id)
        if not post:
            return NotFound
        if post.published == True:
            return self.render_template('/post/%i'%post_id)
        if self.identity.user_id == post.user_id:
            self.update_post_by_fields(post_id, request_publish=True, updated_time=datetime.datetime.utcnow())
            response = Response('Requested. Go back<a href="/post/%s">to the list</a>'%self.identity.username, mimetype='text/html')
            response.status_code=200
            return response
        return Forbidden("")
    @login_required
    def post_delete(self, request, post_id):
        post = self.get_post(post_id)
        if post:
            if self.identity.user_id == post.user_id:
                if request.method == 'POST':
                    self.delete_post(post_id)
                    return redirect("/post/%s"%(self.identity.username))
                else:
                    return Response("Are you sure you want to delete post <i>%s</i>?<br>\
                    <form method='post' action=''><input type='submit' value='yes'></form>\
                    <a href='/post/%i'><button type='button'>no</button></a>"%(post.title,post_id), mimetype="text/html")
            else:
                return Forbidden("")  
        else:
            return NotAcceptable("Invalid data.")
    def authors(self,request):
        users = self.get_all_authors()
        return self.render_template('popular_authors.html', users=users)
    @login_required
    def users_posts(self, request, authorname):
        print('authorname',authorname)
        posts = []
        is_owner = False
        author = self.get_user_by_name(authorname)
        print(author)
        if author:
            ## select all posts from that author

            if self.identity.user_id == author.user_id:
                is_owner = True
                posts = self.get_posts_by_user_id(author.user_id)
            else:
                posts = self.get_public_posts_by_user_id(author.user_id)
            return self.render_template('users_posts.html', posts=posts, is_owner=is_owner)
        return self.render_template('404.html')
    ## database calls

    ## TODO
    def create_admin(self,username:str, password:str)->None:
        ## hash password
        password = generate_password_hash(password, method='sha256') 
        print('Creating <admin %r>...'%username)
        admin = User(username=username, password=password, admin=True)
        self.add_user(admin)
    ## done
    def get_user_by_id(self, id):
        return self.session.query(User).filter_by(user_id=id).first()
    ## done
    def get_user_by_name(self, name):
        return self.session.query(User).filter_by(username=name).first()
    ## done
    def add_user(self, user:User)-> None:
        self.session.add(user)
        self.session.commit()
    ## done - but add sort method
    def get_all_authors(self):
        sql_query = text("SELECT username, count(*) as amount\
                                        FROM posts\
                                        INNER JOIN users on users.user_id = posts.user_id\
                                        WHERE published=1\
                                        GROUP BY posts.user_id\
                                        ORDER BY amount;")
        result = self.session.execute(sql_query)
        return result
    ## done
    def get_post(self, post_id):
        post = self.session.query(Post).filter_by(post_id=post_id).first()
        return post
    ## done
    def post_post(self,post:Post)->None:
        self.session.add(post)
        self.session.commit()
    ## done
    def read_posts(self):
        posts = self.session.query(Post)
        return [p for p in posts]
    ## done
    def get_requested_posts(self):
        return self.session.query(Post).filter_by(request_publish=True).all()
    ## done
    def get_all_public_posts(self):
        result = self.session.query(Post.post_id,Post.title,Post.text, Post.published_time,User.username).join(User).filter(Post.published == True)
        print(result)
        for row in result:
            print(row)
        return [row for row in result]
    ## done
    def get_public_posts_by_user_id(self, user_id):
        return self.session.query(Post).filter_by(user_id = user_id, published = True).all()
    ## done
    def get_posts_by_user_id(self, user_id):
        posts = self.session.query(Post).filter(Post.user_id == user_id).all()
        print("author posts:",posts)
        return [p for p in posts]
    ## TODO
    def update_post_by_fields(self, post_id, **kwargs):
        print("updating post with id", post_id)
        post = self.session.query(Post).filter_by(post_id=post_id).first()
        for attr, value in kwargs.items():
            setattr(post, attr, value)
        for attr in kwargs:
            print(getattr(post, attr))
        self.session.commit()

    # def update_post(self, post:Post): ## deprecated ## does not work
    #     post_id = post.post_id
    #     try:
    #         old_post = self.session.query(Post).filter_by(post_id=post_id).first()
    #         old_post.title = post.title
    #         old_post.text = post.text
    #         old_post.request_publish = post.request_publish
    #         old_post.published = post.published
    #         old_post.updated_time = post.updated_time
    #         old_post.published_time = post.published_time
    #         self.session.commit()
    #     except:
    #         print("Post with post id: %s does not exist" % post_id)
    ## done
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
            "about":self.about,
            "logout":self.logout,
            "post/new":self.post_new,
            "post/edit":self.post_edit,
            "post": self.post,
            "post/authorname":self.users_posts,
            "post/request_publish":self.request_publish,
            "post/publish":self.post_publish,
            "post/delete":self.post_delete,
            "authors":self.authors,
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