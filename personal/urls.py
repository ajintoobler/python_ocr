from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^password-login/$', views.login),
    url(r'^insert/$', views.insert),

]
