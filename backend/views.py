
from .utils import render
from .status_codes import error500, ok200
import psycopg2
def home(environ, start_response):
    return render(environ, start_response, 'static/index.html')

def signup(environ, start_response):
    return render(environ, start_response, 'static/signup.html')

def login(environ, start_response):
    if environ.get('REQUEST_METHOD').lower() == 'post':
        params = environ.get('params')
        if params['username'] == 'aska':
            environ['PATH_INFO'] = '/main'
            environ['REQUEST_METHOD'] = 'GET'
            return main(environ, start_response)
        else:
            return home(environ, start_response)
    return render(environ, start_response, 'static/login.html')

def main(environ, start_response):
    return render(environ, start_response, 'static/main.html')



def about(environ, start_response):
    return render(environ, start_response, 'static/about.html')    

def data(environ, start_response): 
    conn = psycopg2.connect("dbname=test user=postgres password=1valera1 port=5432")
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    except:
        pass
    if environ.get('REQUEST_METHOD').lower() == 'post':
        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
        return ok200(environ, start_response)
    else:
        cur.execute("SELECT * FROM test;")
        start_response('200 OK', [('Content-Type','text/plain')])
        return [b"\n".join([ " ".join([r for r in record]) for record in cur])]