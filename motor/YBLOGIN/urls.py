from django.urls import include, path
from django.contrib.auth import logout
from YBLOGIN import views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="authentication"),
    path("login/", views.login, name="authentication"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    # path('check_hashlink', views.check_hashlink, name='check_hashlink'),
    path("check_hashlink/<str:hash>/<str:type>", views.check_hashlink, name="check_hashlink"),
    path("check_hashlink/<str:hash>/<str:type>/", views.check_hashlink, name="check_hashlink"),
    path("check_hashlink", views.check_hashlink, name="check_hashlink"),
    path("check_hashlink/", views.check_hashlink, name="check_hashlink"),
    # path('signup', views.signup_request, name='signup'),
    # path('account/', views.account_request, name='account'),
    path("logout", logout, name="logout"),
    path("getToken", views.token_auth, name="getToken"),
    path("end_point/<str:name>/<str:action>", views.end_point, name="end_point"),
    path("end_point/<str:name>/<str:action>/", views.end_point, name="end_point"),
]
# url=r'(?P<modulo>\w+)/(?P<pk>\w+)/(?P<accion>\w+)',
