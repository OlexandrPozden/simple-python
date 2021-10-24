from .application import create_app
from .models import initdb, create_admin
def make_app():
    return create_app()