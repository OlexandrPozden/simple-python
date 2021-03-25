
from .utils import render
from .status_codes import error500, ok200
import psycopg2
from .models import ConnectPg, HOSTNAME
import time
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
    a = time.time()
    conn = psycopg2.connect(dbname="postgres", user='postgres', password="1valera1", port=5432, host=HOSTNAME)
    b = time.time()
    print("Time takes to connect to database: {:.5f}".format(b-a))
    #conn = ConnectPg.conn
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
    b = time.time()
    print("To get cursor: {:.5f}".format(b-a))
    print(cur)
    # try:
    #     cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    # except:
    #     conn.rollback()
    # else:
    #     conn.commit()
    if environ.get('REQUEST_METHOD').lower() == 'post':
        # try:
        #     cur.execute("INSERT INTO test (num, data) VALUES (%s, %s);",(100, "abc'def"))
        # except:
        #     conn.rollback()
        # else:
        #     conn.commit()

        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s);",(100, "abc'def"))    
        b = time.time()
        print("To execute command: {:.5f}".format(b-a))
        conn.commit()
        b = time.time()
        print("To commit: {:.5f}".format(b-a))

        cur.close()
        conn.close()
        b = time.time()
        print("To close connection: {:.5f}".format(b-a))
        
        a = time.time()
        start_response('200 OK', [('Access-Control-Allow-Origin','*'),('Content-Type','text/plain')])
        
        b = time.time()
        print("200ok start_response: {:.5f}".format(b-a))
        return [b'200 OK']
    else:
        cur.execute("SELECT * FROM test;")
        b = time.time()
        print("To execute GET command: {:.5f}".format(b-a))
        response_body = "\n".join([ " ".join([str(r) for r in record]) for record in cur])
        cur.close()
        conn.close()
        b = time.time()
        print("To close connection: {:.5f}".format(b-a))
        
        start_response('200 OK', [('Content-Type','text/plain')])
        
        b = time.time()
        print("Start response: {:.5f}".format(b-a))
        return [response_body.encode()]