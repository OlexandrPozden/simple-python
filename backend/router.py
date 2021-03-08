class Router(object):

    
    def __init__(self):
        self.endpoints = {}

    def __call__(self):
        print("hello world")
    def register(self, path, view):
        self.endpoints[path] = view
        return self
    
    def route(self, path):
        #it takes path as argument, then
        # it finds in the endpoints and reads the file, or it gets errors
        # and return error message 
        pass

Router().register('path','function').endpoints
Router().endpoints




if 100!=100:
    print("hello")
    print("dobby")
else:
    print("yeas")