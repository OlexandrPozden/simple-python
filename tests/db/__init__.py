import unittest
from application.application import *

class TestPostSave(unittest.TestCase):
    def setUp(self):
        ## create test objects
        self.test_obj = Post(title="TestObject",text="TestText",user_id=1)
        
    def test_save(self):
        ## save in db
        Post.save(self.test_obj)
        self.assertTrue(self.test_obj.post_id, "Object has not saved in db")
class TestPostGetDelete(unittest.TestCase):    
    def test_query(self):
        test_obj = Post.query().filter().order_by(Post.post_id.desc()).limit(1).first()
        self.assertTrue(test_obj,f'Object with id {test_obj.post_id} does not exist')
    def test_delete(self):
        test_obj = Post.query().filter().order_by(Post.post_id.desc()).limit(1).first()
        test_obj.delete()
        self.assertFalse(test_obj.__dict__,f"Object still has values:\n{test_obj.__dict__}")

    