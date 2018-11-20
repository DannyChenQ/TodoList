from django.conf.urls import *

import views

urlpatterns = [
	url(r'^add/$', views.add, name="add"),
	url(r'^complete/$', views.complete, name="complete"),
	url(r'^delete/$', views.delete, name="delete"),
	url(r'^update/$', views.update, name="update"),
	url(r'^search/$', views.search, name="search"),
	url(r'^login/$', views.log_in, name="login"),
	url(r'^$', views.mytodolist, name="my todo list"),
	url(r'^logout/$', views.log_out, name="logout"),
	url(r'^reg/$', views.registered, name="registered"),
	# url(r'^static/(?P<path>.*)$', 'django.views.static.server', {'document_root': settings.STATIC_ROOT}, name='static'),

]
