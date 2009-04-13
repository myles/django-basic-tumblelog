from datetime, time

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from tumblelog.models import Post

def index(request, page=1, context={}, template_name='tumblelog/index.html'):
	"""
	The Tumblelog index page.
	
	context
		Any extra context you wish to add to this page.
	
	template_name
		If you want to add a custom template to this page.
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
	
	response_type
		The type of response you will want back.
		Current support for HTML and JSON.
	
	context
		Any extra context you wish to add to this page.
	
	template_name
		If you want to add a custom template to this page.
	"""
	try:
		post = Post.objects.get(pk=post_pk)
	except Post.DoesNotExist:
		raise Http404
	
	context.update({
		'post': post,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))