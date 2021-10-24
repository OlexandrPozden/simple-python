'''models.py

Here are stored all models and some functions to interact with them.

Models
------    
User :
        - user_id
        - username
        - password
        - admin
Post :
        - post_id
        - title
        - text
        - user_id
        - published
        - request_publish
        - published_time
        - created_time
        - updated_time'''

import getpass
import datetime


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey  

from werkzeug.security import generate_password_hash
from .keys import DATABASE_URL

base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
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
        id_field = cls.__name__.lower()+"_id"
        return session.query(cls).filter(getattr(cls,id_field) == id).first()
    @classmethod
    def _get_by_field(cls,**field):
        """Returns orm object from db by searched field

        Pass only one argument!
        User.get_by_field(username="Bob")
        Post.get_by_field(title="my first post")
        User.get_by_field(admin=True)

        Returns
        -------
            orm_object
        """
        if len(field) == 1:
            field_name, value  = list(field.items())[0]
            if hasattr(cls, field_name):
                result = session.query(cls).filter(getattr(cls, field_name) == value)
                return result 
            else:
                raise ValueError(f"Field {field_name} does not exist in context of {cls.__name__} model.")
        else:
            raise ValueError(f"Expected lenght of fields 1, but got {len(field)}")
    
    @classmethod
    def get_by_field(cls,**field)->list:
        """Return list or single object of cls model
        
        Queries by only one parameter.
        
        Returns
        -------
            list of orm objects"""
        result = cls._get_by_field(**field).all()
        return result 
    @classmethod
    def get_by_fields(cls,**fields)->list:
        """The same as get_by_field but for many parameters.
        
        It is only name convention. When you search by only field you use
        get_by_field method unless you use get_by_fields.
        Returns
        -------
            list of orm objects"""
        result = None
        for field in fields:
            filter = dict([field]) 
            if not result:
                result = cls._get_by_field(filter)
            else:
                result = result.filter(filter)
        if result:
            return result.all()
        return result
           
    @classmethod
    def delete_by_id(cls,id):
        """Deletes object by id
        
        Examples
        --------
        
        >>>Post.delete_by_id(1013)
        >>>"""
        id_field = cls.__name__.lower()+"_id"
        session.query(cls).filter(getattr(cls,id_field) == id).delete()
        session.commit()
    @classmethod
    def delete_obj(cls,obj):
        """Delete object from the database

        Pass instance of the class to delete that object from the database.
        It looks for id of object and deletes it by id using method delete_by_id.
        If you have object id better use function delete_by_id

        Parameters
        ----------
        
        obj : User, Post
            instance of the model class
        
        Raises
        ------
            - Wrong object type. Raises when you try to delete object using another
            model class.
            - Object does not exist in database.


        Examples
        --------

        >>>isinstance(obj_user, User)
        ... True
        >>>User.delete_obj(obj_user)
        >>>
        """
        id_field = cls.__name__.lower()+"_id"
        id = getattr(obj,id_field)
        if cls.get_by_id(id):
            if isinstance(obj,cls):
                cls.delete_by_id(id)
            else:
                raise Exception(f"Wrong object type. Expected instance of class {cls.__name__} but got {type(obj).__name__}")
        else:
            raise Exception(f"Object {obj.__repr__()} does not exist in database")
    def delete(self):
        """Delete obj from db
        
        The same as delete_obj but for instance of class
        
        Examples
        --------
        
        >>>user_obj.delete()
        >>>user_obj
        >>>"""
        self.delete_obj(self)
        session.commit()
        self.__dict__ = {}
    def update(self,**fields):
        """Update object by field(s)
        
        Specify field_name and value which will be updated.
        
        Examples
        --------

        >>>post_obj.update(title="New title")
        >>>
        
        Parametres
        ----------
        
        fields : **dict, optional

        Raises
        ------

            - AttributeError. Object does not have that field.
        """
        for field in fields.items():
            field_name, value = field
            if hasattr(self, field_name):
                setattr(self, field_name,value)
            else:
                raise AttributeError(f"Object {self} does not have attribute {field_name}")
        session.commit()
    @classmethod
    def query(cls):
        """Write your own custom queries
        
        Examples
        --------
        
        >>>Post.query().filter().order_by(Post.post_id.desc()).limit(1).first()
        <Post post_id='12'>
        >>>"""
        return session.query(cls).filter()

class DbUserManipulation(DbManipulation):
    @classmethod
    def get_user(cls, **kwargs):
        u = User.get_by_field(**kwargs)
        if u:
            return u[0]
        return u
class DbPostManipulation(DbManipulation):
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

## MODELS
class User(base,DbUserManipulation):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        if self.admin:
            return '<Admin username\'%r\'>' % self.username
        return '<User username=\'%r\'>' % self.username
    
class Post(base,DbPostManipulation):
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
        return '<Post post_id=\'%r\'>' % self.post_id

def create_admin():
    username = input("username: ")
    password = getpass.getpass("password: ")
    ## hashing password
    password = generate_password_hash(password, method='sha256')
    ## check if username is already taken
    if not User.get_by_field(username=username)[0]:
        ## create new user with admin privileges
        new_admin = User(username=username, password=password, admin=True)
        User.save(new_admin)
        print("Admin successfuly created!")
    else:
        raise Exception(f"User with username {username} already exists.")
