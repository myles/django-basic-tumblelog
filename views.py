from tagging.views import tagged_object_list

from django.http import Http404
from django.views.generic import list_detail, date_based
from django.contrib.contenttypes.models import ContentType

from tumblelog.models import Item, Event

def item_list(request, page=0):
	return list_detail.object_list(
		request,
		queryset = Item.objects.all(),
		paginate_by = 10,
		page = page,
	)

def item_detail(request, item_id):
	return list_detail.object_detail(
		request,
		queryset = Item.objects.all(),
		object_id = item_id,
		template_name = 'tumblelog/item_detail.html',
	)

def item_list_by_content(request, slug):
	try:
		content_type = ContentType.objects.get(model__iexact=slug, app_label__iexact='tumblelog')
	except ContentType.DoesNotExist:
		raise Http404
	
	return list_detail.object_list(
		request,
		# queryset = Item.objects.by_object(content_type_id=content_type_id),
		queryset = content_type.item_set.all(),
		paginate_by = 10,
		template_name = 'tumblelog/item_list_by_content.html',
		extra_context = { 'content_type' : content_type },
	)

def tags(request, tag):
	return tagged_object_list(
		request,
		model = Item,
		tag = tag,
		template_name = 'tumblelog/tag_detail.html',
	)
