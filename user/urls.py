from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login/',views.login_view),
    path('login_post/',views.login_post,name='login'),
    path('logout/',views.logout_view)

]