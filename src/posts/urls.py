from django.conf.urls import url
from django.contrib import admin

from . views import(
#passing the callable
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete
	)

urlpatterns = [
    #map to the views
    url(r'^$', post_list, name='List'),
    #url(r'^list/$', post_list),
    url(r'^create/$', post_create),
    #<change>, views/postdetail(request, change=None),
    #models/class Post/kwargs={"change":...},
    #templates/index change=obj.id%
    #regex to query                     named url
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]