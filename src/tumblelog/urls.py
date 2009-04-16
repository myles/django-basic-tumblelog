"""
Copyright 2009 Myles Braithwaite <me@mylesbraithwaite.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('tumblelog.views',
	url(r'^post/(?P<obj_pk>\d+)/$',
		view = 'detail',
		name = 'tumblelog_detail',
	),
	# TODO Add a redirect for post/ to tumblelog_index.
	
	url(r'^archive/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
		view = 'archive',
		name = 'tumblelog_archive_month'
	),
	url(r'^archive/(?P<year>\d{4})/$',
		view = 'archive',
		name = 'tumblelog_archive_year'
	),
	url(r'^archive/$',
		view = 'archive',
		name = 'tumblelog_archive_index'
	),
		
	url(r'^page/(?P<page>\w)/$',
		view = 'index',
		name = 'tumblelog_index_paginated',
	),
	url(r'^$',
		view = 'index',
		name = 'tumblelog_index',
	),
)