import os

database_url = str(os.environ["DATABASE_URL"])
i = database_url.find("://") ## add driver
DATABASE_URL = database_url[:i]+"ql+psycopg2"+database_url[i:]
SECRET_KEY = os.environ["SECRET_KEY"]
