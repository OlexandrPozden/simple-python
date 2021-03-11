from .views import login, signup, home
urlpatterns = {
    ('get','/login/'): login,
    ('get','/signup/'): signup,
    ('get','/'): home,
}