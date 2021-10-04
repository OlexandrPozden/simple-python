from .models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import expose, render_template

@expose('/main')
def main(request):
    posts = Post.full_details(published=True)
    error = ""
    username = None
    # posts = self.read_posts()

    # if self.identity:
    #     username = self.identity.username
    # return self.render_template('main.html', posts=posts, error=error, username=username)
    return render_template('main.html', posts=posts, error=error, username=username)


@expose('/signup')
def signup(request):
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ## check if user already exist
        ## if not register new one
        user = User.get_user(username=username)
        # if user:
        #     ## need some flash to show this
        #     error = "User already registered. Please, use another username."
        #     return render_template('signup.html', error=error)
        # else:
        #     new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        #     User.save(new_user)
        #     response = login_user(new_user) ## method login_user already returns response
        #     return response
    return render_template('signup.html')

@expose('/')
def index(request):
    return render_template('index.html')

@expose('/about')
def about(request):
    return render_template('about.html')

@expose('/login')
def login(request):
    error=""
    if request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')

        #user = self.get_user_by_name(username)
        user = User.get_user(username=username) ## we use substracting, because result is list
        # if not user or not check_password_hash(user.password, password): 
        #     error = "Wrong credentials."
        #     return self.render_template('login.html', error=error)
        # else:
        #     ## return token and render template
        #     response = self.login_user(user)
        #     return response
    return render_template('login.html', error=error)