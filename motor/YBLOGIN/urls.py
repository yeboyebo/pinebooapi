from django.urls import include, path
from django.contrib.auth import logout
from YBLOGIN import views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.auth_login, name='authentication'),
    path('login/', views.auth_login, name='authentication'),
    path('signup', views.signup_request, name='signup'),
    path('account/', views.account_request, name='account'),
    path('logout', logout, name='logout'),
    path('getToken', views.token_auth, name='getToken'),
]