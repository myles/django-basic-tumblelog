from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from tumblelog.models import Post

class TumblelogItemFeed(Feed):
	_site = Site.objects.get_current()
	title = _('%s feed') % _site.name
	description = _('%s posts feed.') % _site.name
	
	def link(self):
		return reverse('tumblelog_index')
	
	def items(self):
		return Post.objects.all()[:20]
	
	def item_pubdate(self, item):
		return item.publish