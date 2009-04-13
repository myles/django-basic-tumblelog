from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from tagging.fields import TagField
import tagging

from tumblelog.managers import *

class Item(models.Model):
	""" Item model """
	content_type	= models.ForeignKey(ContentType)
	object_id		= models.PositiveIntegerField()
	content_object	= generic.GenericForeignKey()
	
	author			= models.ForeignKey(User, blank=True, null=True, verbose_name=_('author'))
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	
	tags			= TagField()
	objects			= ItemManager()
	
	class Meta:
		verbose_name		= _('item')
		verbose_name_plural	= _('items')
		db_table			= 'tumblelog_items'
		ordering			= ('-publish',)
		get_latest_by		= 'publish'
	
	def __unicode__(self):
		return u"%s" % self.content_object.title
	
	@permalink
	def get_absolute_url(self):
		return ('tumblelog_item_detail', None, {
			'content_type'	: self.content_type,
			'item_id'		: self.id,
		})