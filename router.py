class Router(object):

    
    def __init__(self, path):
        self.patho = path

    @property
    def path0(self):
        return self.patho
    def __str__(self):
        return self.patho

a = Router("path")
print(a)
a.path0