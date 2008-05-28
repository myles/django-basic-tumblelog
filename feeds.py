from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from tumblelog.models import Item

class TumblelogItemFeed(Feed):
	_site = Site.objects.get_current()
	title = '%s feed' % _site.name
	description = '%s posts feed.' % _site.name
	
	def link(self):
		return reverse('tumblelog_index')
	
	def items(self):
		return Item.objects.all()[:10]
	
	def item_pubdate(self, item):
		return item.publish

class TumblelogByContent(Feed):
	_site = Site.objects.get_current()
	title = "%s feed" % _site.name
	description = '%s posts feed.' % _site.name
	
	def get_objects(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
		
		return ContentType.objects.get(model__iexact=bits[-1], app_label__iexact='tumblelog')
	
	def items(self, obj):
		content_type = ContentType.objects.get(model__iexact=obj.slug, app_label__iexact='tumblelog')
		return content_type.item_set.all()
	
	def link(self, obj):
		return obj.get_absolute_url()
