from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^type/(?P<slug>[-\w]+)/$',
		view	= 'tumblelog.views.item_list_by_content',
		name	= 'item_list_by_content',
	),
	url(r'^archive/(?P<item_id>\d+)/$',
		view	= 'tumblelog.views.item_detail',
		name	= 'tumblelog_item_detail',
	),
	url(r'^page/(?P<page>\w)/$',
		view 	= 'tumblelog.views.item_list',
		name 	= 'tumblelog_index_paginated',
	),
	url(r'^$',
		view	= 'tumblelog.views.item_list',
		name	= 'tumblelog_index',
	),
)