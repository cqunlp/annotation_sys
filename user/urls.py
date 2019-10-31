from django.urls import path,include
from rest_framework import routers

from . import views
router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
app_name = 'user'
urlpatterns = [
    path('login/',views.login_view),
    path('login_post/',views.login_post,name='login'),
    path('logout/',views.logout_view),
    path('reg/', views.reg),
    path('', include(router.urls)),


]