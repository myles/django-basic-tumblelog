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