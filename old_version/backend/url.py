from .views import login, signup, home,data
urlpatterns = {
    ('get','/login'): login,
    ('get','/signup'): signup,
    ('get','/'): home,
    ('post','/login'): login,
    ('post','/data'): data,
    ('get','/data'): data,
}

# url = {
#     {'/path':}
# }