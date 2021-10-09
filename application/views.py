from .models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException, NotFound, Forbidden, NotAcceptable
from .utils import expose, render_template, login_required, admin_required, Response
from werkzeug.utils import redirect
import datetime

from .models import User, Post
from .utils import Auth

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
        if user:
            error = "User already registered. Please, use another username."
            return render_template('signup.html', error=error)
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
            User.save(new_user)
            response = Auth.login_user(new_user,redirect(f"/user/{new_user.username}")) ## method login_user already returns response
            return response
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
        if not user or not check_password_hash(user.password, password): 
             error = "Wrong credentials."
             return render_template('login.html', error=error)
        else:
             response = Auth.login_user(user, redirect(f"/user/{user.username}"))
             return response
    return render_template('login.html', error=error)

@expose('/logout')
def logout(request):
    if request.identity.logged_in:
        return Auth.logout_user(response=redirect("/main"))
    return Forbidden("You need to be logged in.")
@admin_required
@expose('/admin')
def admin(request):
    posts = Post.get_by_field(request_publish=True)
    return render_template('admin.html',posts=posts)
@login_required
@expose('/post/new')
def post_new(request):
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        request_publish = bool(request.form.get('request_publish'))
        user_id = request.identity.user_id
        username = request.identity.username

        post = Post(title=title, text=text, request_publish = request_publish, user_id=user_id)
        Post.save(post)

        return redirect('/post/%s'%username)

    return render_template('new_post.html',post=None)
@login_required
@expose('/post/<int:post_id>/edit')
def post_edit(request, post_id:int):
    
    post = Post.get_by_id(post_id)

    if request.method == 'POST':
        request_publish = bool(request.form.get('request_publish'))
        title = request.form.get('title')
        text = request.form.get('text')
        
        post.update(
        title=title,
        text=text,
        request_publish=request_publish,
        published=False,
        updated_time = datetime.datetime.utcnow()
        )

        return redirect('/post/%s'%self.identity.username)
        
    if post:
        ## is author of that post
        if post.user_id == request.identity.user_id: 
            return render_template('new_post.html', post=post)
    return render_template('404.html')
@login_required
@expose('/post/<int:post_id>')
def post(request, post_id):
    is_owner = False
    is_admin = False

    post = Post.get_by_id(post_id)

    if post: 
        if request.identity.user_id == post.user_id: 
            is_owner = True
        is_admin = request.identity.admin
        return render_template('post.html', post=post,is_owner=is_owner, is_admin=is_admin)
    return render_template('404.html')

@admin_required
@expose('/post/<int:post_id>/publish')
def post_publish(request, post_id):
    post = Post.get_by_id(post_id)

    if not post: 
        return NotFound("Post with id '{}' not found.".format(post_id))
    else:
        if not post.request_publish:
            return redirect('/admin') 

        post.update(request_publish=False,
        published=True, 
        published_time=datetime.datetime.utcnow())

        return redirect('/admin')

@login_required
@expose('/post/<int:post_id>/request')
def request_publish(request, post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return NotFound("Post with id '{}' not found.".format(post_id))
    if post.published == True:
        return render_template('/post/%i'%post_id)
    if request.identity.user_id == post.user_id:

        post.update( 
        request_publish=True, 
        updated_time=datetime.datetime.utcnow())

        response = Response('Requested. Go back<a href="/post/%s">to the list</a>'%request.identity.username, mimetype='text/html')
        response.status_code=200
        return response
    return Forbidden("")
@login_required
@expose('/post/<int:post_id>/delete')
def post_delete(request, post_id):
    post = Post.get_by_id(post_id)
    if post:
        if request.identity.user_id == post.user_id:
            if request.method == 'POST':
                post.delete()
                return redirect("/post/%s"%(request.identity.username))
            else:
                return Response("Are you sure you want to delete post <i>%s</i>?<br>\
                <form method='post' action=''><input type='submit' value='yes'></form>\
                <a href='/post/%i'><button type='button'>no</button></a>"%(post.title,post_id), mimetype="text/html")
        else:
            return Forbidden("")  
    else:
        return NotAcceptable("Invalid data.")
    
@login_required
@expose('/user/<string:authorname>')
def users_posts(request, authorname):
    posts = []
    is_owner = False

    author = User.get_user(username=authorname)
    
    if author:
        ## select all posts from that author

        if request.identity.user_id == author.user_id:
            is_owner = True
            posts = Post.get_by_field(user_id=author.user_id)
        else:
            ## HERE
            posts = Post.query().join(User).filter(User.user_id == author.user_id, Post.published == True).order_by(Post.published_time.desc()).all()
        return render_template('users_posts.html', posts=posts, is_owner=is_owner)
    return render_template('404.html')
@expose('/authors')
def authors(request):
    ## HERE TODO
    ## NEED aggregation function
    users = Post.full_details(published=True)
    return render_template('popular_authors.html', users=users)