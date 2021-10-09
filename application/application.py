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

## REMOVE
# def admin_required(fun):
#     def wrapper(*args, **kwargs):
#         self = args[0]
#         if self.identity:
#             if self.identity.admin:
#                 return fun(*args, **kwargs)
#         return Forbidden('Only users with admin permission can reach this page.')
#     return wrapper
# def login_required(fun): 
#     def wrapper(*args, **kwargs):
#         self = args[0]
#         request = args[1]
#         if self.identity.logged_in:
#             return fun(*args, **kwargs)
#         else:
#             self.turn_back_to = request.path
#             return redirect('/login')
#     return wrapper
## REMOVE
# def create_token(payload):
#     payload['exp'] = datetime.datetime.utcnow()+datetime.timedelta(seconds=300)
#     token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
#     return token

# def payload_from_token(token):
#     payload = {}
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         print("Token is still valid and active")
#     except jwt.ExpiredSignatureError:
#         print("Token expired. Get new one")
#     except jwt.InvalidTokenError:
#         print("Invalid Token")
#     return payload

class Application(object):
    def __init__(self, config=None):
        
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True
        )
        ## REMOVE
        # self.url_map = Map(
        #     [
        #         Rule("/", endpoint="index"),
        #         Rule("/login", endpoint="login"),
        #         Rule("/main", endpoint="main"),
        #         Rule('/signup', endpoint="signup"),
        #         Rule('/admin', endpoint="admin"),
        #         Rule('/logout', endpoint="logout"),
        #         Rule('/about', endpoint="about"),
        #         Rule('/post', endpoint="main"),
        #         Rule('/post/<int:post_id>', endpoint="post"),
        #         Rule('/post/<int:post_id>/edit', endpoint="post/edit"),
        #         Rule('/post/new', endpoint="post/new"),
        #         Rule('/post/<string:authorname>', endpoint="post/authorname"),
        #         Rule('/post/<int:post_id>/request_publish', endpoint="post/request_publish"),
        #         Rule('/post/<int:post_id>/publish', endpoint="post/publish"),
        #         Rule('/post/<int:post_id>/delete', endpoint="post/delete"),
        #         Rule('/authors', endpoint="authors")
        #     ]
        # )

        ## REMOVE UPDATE
        # self.turn_back_to = "" ## turn back to page where user was redirected from
        
        # self.identity = None ## <class 'User'> if logged in

    ## REMOVE
    # ## custom functions
    # @property
    # def path_to_turn_back(self):
    #     if self.turn_back_to:
    #         path = self.turn_back_to
    #         self.turn_back_to = ""
    #         return path
    #     return self.turn_back_to
    # def login_user(self, user, redirect_to=None):
    #     token = create_token(self._create_payload_from_user(user))
    #     response = redirect(self.path_to_turn_back or redirect_to or '/main')
    #     response.set_cookie("token",token)
    #     return response
    # def logout_user(self, response:Response)->Response:
    #     if self.identity:
    #         self.identity = None
    #         response.delete_cookie("token")
    #     return response
    # def _create_payload_from_user(self, user:User)->dict:
    #     return {'sub':user.user_id,'username':user.username}
    # def _identity_check(self, request):
    #     token = request.cookies.get('token', None)
    #     if token:
    #         payload = payload_from_token(token)
    #         if payload:
    #             user_id = payload.get('sub','')
    #             username = payload.get('username','')
    #             user = User.get_by_id(user_id)
    #             if user:
    #                 if user.username == username:
    #                     self.identity = user

    ## REMOVE CAUTION
    # ## views     
    # def index(self,request):
    #     return self.render_template('index.html')
    # def about(self,request):
    #     return self.render_template('about.html')
    # def login(self,request):
    #     error=""
    #     if request.method == 'POST':
    #         username = request.form.get('username','')
    #         password = request.form.get('password','')

    #         #user = self.get_user_by_name(username)
    #         user = User.get_user(username=username) ## we use substracting, because result is list
    #         if not user or not check_password_hash(user.password, password): 
    #             error = "Wrong credentials."
    #             return self.render_template('login.html', error=error)
    #         else:
    #             ## return token and render template   
    #             response = Auth.login_user(user,redirect("/main"))
    #             return response
    #     return self.render_template('login.html', error=error)
    # def logout(self,request):
    #     return self.logout_user(redirect('/'))
    # def main(self,request):
    #     posts = Post.full_details(published=True)
    #     error = ""
    #     username = None
    #     # posts = self.read_posts()

    #     if self.identity:
    #         username = self.identity.username
    #     return self.render_template('main.html', posts=posts, error=error, username=username)
    
    # def signup(self,request):
    #     error = ''
    #     if request.method == 'POST':
    #         username = request.form['username']
    #         password = request.form['password']
    #         ## check if user already exist
    #         ## if not register new one
    #         user = User.get_user(username=username)
    #         if user:
    #             ## need some flash to show this
    #             error = "User already registered. Please, use another username."
    #             return self.render_template('signup.html', error=error)
    #         else:
    #             new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
    #             User.save(new_user)
    #             response = self.login_user(new_user) ## method login_user already returns response
    #             return response
    #     return self.render_template('signup.html')
    # @admin_required
    # def admin(self,request):
    #     posts = Post.get_by_field(request_publish=True)
    #     return self.render_template('admin.html',posts=posts)
    # @login_required
    # def post_new(self, request):
    #     if request.method == 'POST':
    #         title = request.form.get('title')
    #         text = request.form.get('text')
    #         request_publish = bool(request.form.get('request_publish'))
    #         user_id = self.identity.user_id
    #         username = self.identity.username

    #         post = Post(title=title, text=text, request_publish = request_publish, user_id=user_id)
    #         Post.save(post)

    #         return redirect('/post/%s'%username)

    #     return self.render_template('new_post.html',post=None)
    # @login_required
    # def post_edit(self, request, post_id:int):
        
    #     post = Post.get_by_id(post_id)

    #     if request.method == 'POST':
    #         request_publish = bool(request.form.get('request_publish'))
    #         title = request.form.get('title')
    #         text = request.form.get('text')
            
    #         post.update(
    #         title=title,
    #         text=text,
    #         request_publish=request_publish,
    #         published=False,
    #         updated_time = datetime.datetime.utcnow()
    #         )

    #         return redirect('/post/%s'%self.identity.username)
            
    #     if post:
    #         ## is author of that post
    #         if post.user_id == self.identity.user_id: 
    #             return self.render_template('new_post.html', post=post)
    #     return self.render_template('404.html')
    # @login_required
    # def post(self, request, post_id):
    #     is_owner = False
    #     is_admin = False

    #     post = Post.get_by_id(post_id)

    #     if post: 
    #         if self.identity.user_id == post.user_id: 
    #             is_owner = True
    #         is_admin = self.identity.admin
    #         return self.render_template('post.html', post=post,is_owner=is_owner, is_admin=is_admin)
    #     return self.render_template('404.html')

    # @admin_required
    # def post_publish(self, request, post_id):
    #     post = Post.get_by_id(post_id)

    #     if not post: 
    #         return NotFound("Post with id '{}' not found.".format(post_id))
    #     else:
    #         if not post.request_publish:
    #             return redirect('/admin') 

    #         post.update(request_publish=False,
    #         published=True, 
    #         published_time=datetime.datetime.utcnow())

    #         return redirect('/admin')

    # @login_required
    # def request_publish(self, request, post_id):
    #     post = Post.get_by_id(post_id)
    #     if not post:
    #         return NotFound("Post with id '{}' not found.".format(post_id))
    #     if post.published == True:
    #         return self.render_template('/post/%i'%post_id)
    #     if self.identity.user_id == post.user_id:

    #         post.update( 
    #         request_publish=True, 
    #         updated_time=datetime.datetime.utcnow())

    #         response = Response('Requested. Go back<a href="/post/%s">to the list</a>'%self.identity.username, mimetype='text/html')
    #         response.status_code=200
    #         return response
    #     return Forbidden("")
    # @login_required
    # def post_delete(self, request, post_id):
    #     post = Post.get_by_id(post_id)
    #     if post:
    #         if self.identity.user_id == post.user_id:
    #             if request.method == 'POST':
    #                 post.delete()
    #                 return redirect("/post/%s"%(self.identity.username))
    #             else:
    #                 return Response("Are you sure you want to delete post <i>%s</i>?<br>\
    #                 <form method='post' action=''><input type='submit' value='yes'></form>\
    #                 <a href='/post/%i'><button type='button'>no</button></a>"%(post.title,post_id), mimetype="text/html")
    #         else:
    #             return Forbidden("")  
    #     else:
    #         return NotAcceptable("Invalid data.")
    # def authors(self,request):
    #     ## HERE
    #     ## NEED aggregation function
    #     users = Post.full_details(published=True)
    #     return self.render_template('popular_authors.html', users=users)
    # @login_required
    # def users_posts(self, request, authorname):
    #     posts = []
    #     is_owner = False

    #     author = User.get_by_field(username = authorname)[0]
        
    #     if author:
    #         ## select all posts from that author

    #         if self.identity.user_id == author.user_id:
    #             is_owner = True
    #             posts = Post.get_by_field(user_id=author.user_id)
    #         else:
    #             ## HERE
    #             posts = Post.query().join(User).filter(User.user_id == author.user_id, Post.published == True).order_by(Post.published_time.desc()).all()
    #         return self.render_template('users_posts.html', posts=posts, is_owner=is_owner)
    #     return self.render_template('404.html')
    ## database calls

    # ## done
    # def create_admin(self,username:str, password:str)->None:
    #     ## hash password
    #     password = generate_password_hash(password, method='sha256') 
    #     print('Creating <admin %r>...'%username)
    #     admin = User(username=username, password=password, admin=True)
    #     self.add_user(admin)
    # ## done
    # def get_user_by_id(self, id):
    #     return self.session.query(User).filter_by(user_id=id).first()
    # ## done
    # def get_user_by_name(self, name):
    #     return self.session.query(User).filter_by(username=name).first()
    # ## done
    # def add_user(self, user:User)-> None:
    #     self.session.add(user)
    #     self.session.commit()
    # ## done - but add sort method
    # def get_all_authors(self):
    #     sql_query = text("SELECT username, count(*) as amount\
    #                                     FROM posts\
    #                                     INNER JOIN users on users.user_id = posts.user_id\
    #                                     WHERE published=1\
    #                                     GROUP BY posts.user_id\
    #                                     ORDER BY amount;")
    #     result = self.session.execute(sql_query)
    #     return result
    # ## done
    # def get_post(self, post_id):
    #     post = self.session.query(Post).filter_by(post_id=post_id).first()
    #     return post
    # ## done
    # def post_post(self,post:Post)->None:
    #     self.session.add(post)
    #     self.session.commit()
    # ## done
    # def read_posts(self):
    #     posts = self.session.query(Post)
    #     return [p for p in posts]
    # ## done
    # def get_requested_posts(self):
    #     return self.session.query(Post).filter_by(request_publish=True).all()
    # ## done
    # def get_all_public_posts(self):
    #     result = self.session.query(Post.post_id,Post.title,Post.text, Post.published_time,User.username).join(User).filter(Post.published == True)
    #     print(result)
    #     for row in result:
    #         print(row)
    #     return [row for row in result]
    # ## done
    # def get_public_posts_by_user_id(self, user_id):
    #     return self.session.query(Post).filter_by(user_id = user_id, published = True).all()
    # ## done
    # def get_posts_by_user_id(self, user_id):
    #     posts = self.session.query(Post).filter(Post.user_id == user_id).all()
    #     print("author posts:",posts)
    #     return [p for p in posts]
    # ## done
    # def update_post_by_fields(self, post_id, **kwargs):
    #     print("updating post with id", post_id)
    #     post = self.session.query(Post).filter_by(post_id=post_id).first()
    #     for attr, value in kwargs.items():
    #         setattr(post, attr, value)
    #     for attr in kwargs:
    #         print(getattr(post, attr))
    #     self.session.commit()

    # # def update_post(self, post:Post): ## deprecated ## does not work
    # #     post_id = post.post_id
    # #     try:
    # #         old_post = self.session.query(Post).filter_by(post_id=post_id).first()
    # #         old_post.title = post.title
    # #         old_post.text = post.text
    # #         old_post.request_publish = post.request_publish
    # #         old_post.published = post.published
    # #         old_post.updated_time = post.updated_time
    # #         old_post.published_time = post.published_time
    # #         self.session.commit()
    # #     except:
    # #         print("Post with post id: %s does not exist" % post_id)
    # ## done
    # def delete_post(self, post_id):
    #     self.session.query(Post).filter_by(post_id=post_id).delete()
    #     self.session.commit()


     ## additional server functionality
    def _dispatch_request(self,request):
        ## REMOVE
        # endpoint_to_views={
        #     "index":self.index,
        #     "login":self.login,
        #     "main":self.main,
        #     "signup":self.signup,
        #     "admin":self.admin,
        #     "about":self.about,
        #     "logout":self.logout,
        #     "post/new":self.post_new,
        #     "post/edit":self.post_edit,
        #     "post": self.post,
        #     "post/authorname":self.users_posts,
        #     "post/request_publish":self.request_publish,
        #     "post/publish":self.post_publish,
        #     "post/delete":self.post_delete,
        #     "authors":self.authors,
        # }
        adapter = url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
            return response
            ## REMOVE
            #return endpoint_to_views[endpoint](request,**values)
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


