from .views import login, signup, home, logining
urlpatterns = {
    ('get','/login'): login,
    ('get','/signup'): signup,
    ('get','/'): home,
    ('post','/login'): logining
}