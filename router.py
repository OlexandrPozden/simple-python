class Router(object):

    
    def __init__(self):
        self.endpoints = {}

    def register(self, path, file):
        self.endpoints[path] = file
    
    def route(self, path):
        #it takes path as argument, then
        # it finds in the endpoints and reads the file, or it gets errors
        # and return error message 
        pass
