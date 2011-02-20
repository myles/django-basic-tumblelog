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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from tumblelog.managers import PostManager

class Post(models.Model):
	"""Tumblelog Post model.

	:param content_object: A link to the tumblelog object.
	:param title: Cache the title of the object.
	:param author: Cache the author of the object.
	:param publish: Cache the object's Published date.
	:param created: When the tumblelog entry was created.
	:param modified: When the tumblelog entry was modified.
	"""
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey()

	title = models.CharField(_('title'), max_length=200)
	author = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               verbose_name=_('author'),
                               related_name='author_post')
	publish = models.DateTimeField(_('publish'))
	created = models.DateTimeField(_('created'), auto_now_add=True)
	modified = models.DateTimeField(_('modified'), auto_now=True)

	objects = PostManager()

	class Meta:
		verbose_name = _('post')
		verbose_name_plural = _('posts')
		db_table = 'tumblelog'
		ordering = ('-publish',)
		get_latest_by = 'publish'

	def __unicode__(self):
		return u"%s" % self.title

	@permalink
	def get_absolute_url(self):
		return ('tumblelog_detail', None, {
			'post_pk' : self.pk,
		})
