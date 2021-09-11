from werkzeug.wrappers import Request, Response
from flask_jwt import JWT, jwt_required, current_identity

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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import Column, String, Integer  
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

base = declarative_base()
class Post(base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    def __repr__(self):
        return '<Post %r>' % self.post_id

class Application(object):
    def __init__(self, config=None):
        engine = create_engine('sqlite:///test.db', echo=True)
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
            ]
        )
    def index(self,request):
        return self.render_template('index.html')
    def login(self,request):
        if request.method == 'POST':
            username = request.form.get('username','')
            ## get username and password check if 
        return self.render_template('login.html')
    def main(self,request):
        #self.update_post(10,"UPDATED TEXT")
        #self.delete_post(4)
        posts=[]
        if request.method == 'POST':
            text = request.form['text']
            posts = self.post_text(text)
        else:
            posts = self.read_posts()
        return self.render_template('main.html', posts=posts)
    def signup(self,request):
        return self.render_template('signup.html')

    def create_post(self,post:Post):
        self.session.add(post)
        self.session.commit()
    def read_posts(self):
        posts = self.session.query(Post)
        return [p for p in posts]
    def update_post(self, post_id:int, text:str):
        try:
            post = self.session.query(Post).filter_by(post_id=post_id).first()
            post.text = text
            self.session.commit()
        except:
            print("Post with post id: %s does not exist" % post_id)
    def delete_post(self, post_id):
        self.session.query(Post).filter_by(post_id=post_id).delete()
        self.session.commit()

    def post_text(self,text):
        post = Post(text=text)
        self.create_post(post)
        return self.read_posts()
        
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