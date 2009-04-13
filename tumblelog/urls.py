from django.conf.urls.defaults import *

urlpatterns = patterns('',
	#url(r'^post/(?P<obj_pk>\d+)/$',
	#	view = 'tumblelog.views.detail',
	#	name = 'tumblelog_detail',
	#),
	# TODO Add a redirect for post/ to tumblelog_index.
	
	#url(r'^archive/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
	#	view = 'tumblelog.views.archive',
	#	name = 'tumblelog_archive_month'
	#),
	#url(r'^archive/(?P<year>\d{4})/$',
	#	view = 'tumblelog.views.archive',
	#	name = 'tumblelog_archive_year'
	#),
	#url(r'^archive/$',
	#	view = 'tumblelog.views.archive',
	#	name = 'tumblelog_archive_index'
	#),
		
	url(r'^page/(?P<page>\w)/$',
		view = 'tumblelog.views.index',
		name = 'tumblelog_index_paginated',
	),
	url(r'^$',
		view = 'tumblelog.views.index',
		name = 'tumblelog_index',
	),
)