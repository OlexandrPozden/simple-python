import psycopg2
class ConnectPg:
    dbname="test"
    user="postgres"
    password="1valera1"
    port=5432
    conn = None
    @classmethod
    def connect_database(cls):
        print("Connecting to database...")
        try:
            cls.conn = psycopg2.connect(dbname=cls.dbname, user=cls.user, password=cls.password, port=cls.port)
        except:
            print("Failed to connect to database!!!")
        else:
            print("Database is connected")



# class User():
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password