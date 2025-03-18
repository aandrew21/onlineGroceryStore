from django.urls import path
from . import views
from .views import user_login, user_logout, user_register

urlpatterns = [
    path('login/', user_login, name='user-login'),
    path('register/', user_register, name='user-register'),
    path('logout/', user_logout, name='user-logout'),
]
