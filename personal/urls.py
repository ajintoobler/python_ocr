from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^password-login/$', views.login),
    url(r'^insert/$', views.insert),
    url(r'^redirect/$', views.redirect),
    url(r'^userSearchPage/$', views.userSearchpage),
    url(r'^searchpage/$', views.userSearch),
    url(r'^searchpageresult/$', views.userSearchResult),
    url(r'^collectionView/$', views.adminCollectionView),


]
