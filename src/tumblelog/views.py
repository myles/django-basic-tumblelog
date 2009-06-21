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

import datetime, time

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from tumblelog.models import Post

def index(request, page=1, context={}, template_name='tumblelog/index.html'):
	"""
	The Tumblelog index page.
	
	:type page: int
	:param context: Any extra context you wish to add to this page.
	:type context: dict
	:param template_name: If you want to add a custom template to this page.
	:type template_name: string
	"""
	
	post_list = Post.objects.published()
	paginator = Paginator(post_list, 20)
	
	try:
		posts = paginator.page(page)
	except (EmptyPage, InvalidPage):
		posts = paginator.page(paginator.num_pages)
	
	context.update({
		'posts': posts,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def detail(request, post_pk, context={}, template_name='tumblelog/detail.html'):
	"""
	The Tumblelog Post detail page.
	
	:param context: Any extra context you wish to add to this page.
	:type context: dict
	:param template_name: If you want to add a custom template to this page.
	:type template_name: string
	"""
	
	try:
		post = Post.objects.get(pk=post_pk)
	except Post.DoesNotExist:
		raise Http404
	
	context.update({
		'post': post,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def archive(request, year=str(datetime.date.today().year),
	month=datetime.date.today().strftime('%b'), context={},
	template_name='tumblelog/archive.html'):
	"""
	The Tumblelog Post archive page.
	
	:param year: The year you want to filter.
	:type year: string
	:param month: The month you want to filter.
	:type month: string
	:param context: Any extra context you wish to add to this page.
	:type context: dict
	:param template_name: If you want to add a custom template to this page.
	:type template_name: string
	"""
	
	try:
		date = datetime.date(*time.strptime(year+month, '%Y%b')[:3])
	except ValueError:
		raise Http404
	
	posts = Post.objects.filter(publish__month=date.month,
		publish__year=date.year)
	
	context.update({
		'posts': posts,
		'date': date,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))