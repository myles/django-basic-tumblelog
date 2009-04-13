from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from tumblelog.managers import PostManager

class Post(models.Model):
	""" Item model """
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey()
	
	title = models.CharField(_('title'), max_length=200)
	author = models.ForeignKey(User, blank=True, null=True, verbose_name=_('author'))
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
			'obj_pk' : self.pk,
		})