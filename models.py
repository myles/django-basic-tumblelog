import urllib
import urlparse

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import truncatewords_html

from tagging.fields import TagField
import tagging

from tumblelog.managers import *

class Item(models.Model):
	""" Item model """
	content_type	= models.ForeignKey(ContentType)
	object_id		= models.PositiveIntegerField()
	content_object	= generic.GenericForeignKey()
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	
	tags			= TagField()
	objects			= ItemManager()
	
	class Admin:
		pass
	
	class Meta:
		verbose_name = _('item')
		verbose_name_plural = _('items')
		db_table = 'tumblelog_items'
		ordering = ('-publish',)
		get_latest_by = 'publish'
	
	def __unicode__(self):
		return u"%s" % self.content_object.title
	
	@permalink
	def get_absolute_url(self):
		return ('tumblelog_item_detail', None, {
			'content_type'	: self.content_type,
			'item_id'		: self.id,
		})

def save_as_item(self):
	super(self.__class__, self).save()
	try:
		content_type = ContentType.objects.get_for_model(self)
		Item.objects.get(content_type__pk=content_type.id, object_id=self.id)
	except Item.DoesNotExist:
		Item.objects.create(content_object=self, author=self.author, publish=self.publish, tags=self.tags)

def delete_as_item(self):
	try:
		content_type = ContentType.objects.get_for_model(self)
		item = Item.objects.get(content_type__pk=content_type.id, object_id=self.id)
		item.delete()
	except Item.DoesNotExist:
		pass
	super(self.__class__, self).delete()

class Link(models.Model):
	"""
	A link, with an optional commentary.
	"""
	title			= models.CharField(_('title'), null=False, blank=False, max_length=100)
	url				= models.URLField(null=False, blank=False, verbose_name=_('URL'))
	via_title		= models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Via Title'))
	via_url			= models.URLField(null=True, blank=True, verbose_name=_('Via URL'))
	body			= models.TextField(_('body'), null=True, blank=True, help_text=_('Use Textile.'))
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	                
	tags			= TagField()
	
	class Meta:
		verbose_name = _('link')
		verbose_name_plural = _('links')
		ordering = ('-publish',)
		get_latest_by = 'publish'
		db_table = 'tumblelog_link'
	
	class Admin:
		list_display = ('title', 'url', 'author', 'publish')
		list_filter = ('publish', 'author')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='link', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()

Link.save = save_as_item
Link.delete = delete_as_item

class VideoSource(models.Model):
	"""
	A place you might view videos. Basically just an encapsulation for the
	"embed template" bit.
	"""
	title			= models.CharField(_('title'), max_length=200)
	home			= models.URLField(_('home'))
	embed_template	= models.URLField(verify_exists=False)
	
	class Meta:
		verbose_name = _('video source')
		verbose_name_plural = _('video sources')
		db_table = 'tumblelog_video_source'
	
	class Admin:
		list_display = ('title',)
	
	def __unicode__(self):
		return u"%s" % self.title

class Video(models.Model):
	"""
	A video you viewed.
	"""
	source			= models.ForeignKey(VideoSource, related_name="videos")
	title			= models.CharField(_('title'), max_length=200)
	url				= models.URLField(_('url'))
	body			= models.TextField(_('body'), null=True, blank=True, help_text=_('Use Textile.'))
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	                
	tags			= TagField()
	
	class Meta:
		verbose_name = _('video')
		verbose_name_plural = _('videos')
		ordering = ('-publish',)
		get_latest_by = 'publish'
		db_table = 'tumblelog_video'
	
	class Admin:
		list_display = ('title', 'author', 'publish')
		list_filter = ('publish', 'author', 'source')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@property
	def docid(self):
		scheme, netloc, path, params, query, fragment = urlparse.urlparse(self.url)
		return query.split("=")[-1]
	
	@property
	def embed_url(self):
		return self.source.embed_template % self.docid
	
	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='video', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()

Video.save = save_as_item
Video.delete = delete_as_item

class Twitter(models.Model):
	"""
	A twit post.
	"""
	body			= models.CharField(_('body'), max_length=140, help_text="The first five words will be used a the title. Also HTML is okay.")
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	
	tags			= TagField()
	
	class Meta:
		verbose_name = _('twitter')
		verbose_name_plural = _('twitter')
		ordering = ('-publish',)
		get_latest_by = 'publish'
		db_table = 'tumblelog_twitter'
	
	class Admin:
		list_display = ('title', 'author', 'publish')
		list_filter = ('publish', 'author')
	
	@property
	def title(self):
		return truncatewords_html(self.body, "5")
		
	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='twitter', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()

Twitter.save = save_as_item
Twitter.delete = delete_as_item

class Chat(models.Model):
	"""
	A chat log.
	"""
	title			= models.CharField(_('location'), max_length=50, null=True, blank=True, help_text=_('IRC, AIM, Phone, etc.'))
	chat			= models.TextField(_('chat'), null=False, blank=False)
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	                
	tags			= TagField()
	
	class Meta:
		verbose_name = _('chat')
		verbose_name_plural = _('chats')
		ordering = ('-publish',)
		get_latest_by = 'publish'
		db_table = 'tumblelog_chat'
	
	class Admin:
		list_display = ('title', 'author', 'publish')
		list_filter = ('publish', 'author')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	def get_lines(self):
		return [line.strip() for line in self.chat.split('\n')]
	
	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='chat', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()

Chat.save = save_as_item
Chat.delete = delete_as_item

class Event(models.Model):
	title			= models.CharField(_('title'), max_length=200)
	location		= models.TextField(_('location'), blank=True, null=True)
	when			= models.DateTimeField()
	body			= models.TextField(null=True, blank=True)
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	
	tags			= TagField()
	
	class Meta:
		verbose_name = _('event')
		verbose_name_plural = _('events')
		ordering = ("-publish",)
		get_latest_by = 'publish'
	
	class Admin:
		list_display = ('title', 'author', 'publish',)
		list_filter = ('publish', 'author')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='event', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()

Event.save = save_as_item
Event.delete = delete_as_item

class Photo(models.Model):
	"""
	Photo model.
	"""
	title			= models.CharField(_('title'), max_length=200)
	photo			= models.ImageField(_('photo'), upload_to="uploads/tumblelog/o/%Y/%m/%d/")
	photo_tumbnail	= models.ImageField(_('photo thumbnail'), upload_to="uploads/tumblelog/t/%Y/%m/%d/",  editable=False)
	body			= models.TextField(_('caption'), null=True, blank=True)
	link			= models.URLField(_('link'), null=True, blank=True)
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	                
	tags			= TagField()
	
	class Meta:
		verbose_name = _('photo')
		verbose_name_plural = _('photos')
		ordering = ("-publish",)
		get_latest_by = 'publish'
	
	class Admin:
		list_display = ('title', 'author', 'publish',)
		list_filter = ('publish', 'author',)
	
	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='photo', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()
	
	def save(self):
		from PIL import Image
		
		SMALL_SIZE = (240, 240)
		
		if not self.photo_tumbnail:
			self.save_photo_tumbnail_file(self.get_photo_filename(), '')
			image = Image.open(self.get_photo_filename())
			if image.mode not in ('L', 'RGB'):
				image = image.convert('RGBA')
			image.thumbnail(SMALL_SIZE, Image.ANTIALIAS)
			image.save(self.get_photo_tumbnail_filename())
		
		super(Photo, self).save()

Photo.save = save_as_item
Photo.delete = delete_as_item

class Audio(models.Model):
	"""
	Audio model
	"""
	title			= models.CharField(_('title'), max_length=200)
	audio			= models.FileField(_('audio'), upload_to='uploads/tumblelog/audio', blank=True, null=True)
	body			= models.TextField(_('caption'), null=True, blank=True)
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	                
	tags			= TagField()
	
	class Meta:
		verbose_name = _('audio')
		verbose_name_plural = _('audio')
		ordering = ('-publish',)
		get_latest_by = 'publish'
	
	class Admin:
		list_display = ('title', 'author', 'publish')
		list_filter = ('publish', 'author',)
	
	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='audio', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()

Audio.save = save_as_item
Audio.delete = delete_as_item

class Quote(models.Model):
	"""
	Quote model.
	"""
	quote			= models.TextField(_('quote'))
	body			= models.TextField(_('source'), null=True, blank=True)
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	                
	tags			= TagField()
	
	class Meta:
		verbose_name = _('quote')
		verbose_name_plural = _('quotes')
		ordering = ('-publish',)
		get_latest_by = 'publish'
	
	class Admin:
		list_display = ('title', 'author', 'publish')
		list_filter = ('publish', 'author')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@property
	def title(self):
		return truncatewords_html(self.quote, "5")

	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='quote', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()

Quote.save = save_as_item
Quote.delete = delete_as_item

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, LEXERS
from pygments.styles import STYLE_MAP
from pygments.styles import colorful

LANGUAGES = [(x[2][0], x[1]) for x in LEXERS.itervalues()]
LANGUAGES.sort(key=lambda x: x[1].lower())

STYLES = [(x, x.title()) for x in STYLE_MAP]
STYLES.sort(key=lambda x: x[0].lower())
KNOWN_STYLES = set(STYLE_MAP)

formatter = HtmlFormatter(cssclass='syntax', linenos=True, encoding='utf-8', linenospecial=5)

class Snippet(models.Model):
	"""
	A code snippet model.
	"""
	title			= models.CharField(_('title'), max_length=200)
	body			= models.TextField(_('body'), null=True, blank=True)
	syntax			= models.CharField(_('syntax'), max_length=20, null=False, blank=False, choices=LANGUAGES, default='text')
	code			= models.TextField(null=False, blank=False)
	
	author			= models.ForeignKey(User, blank=True, null=True)
	publish			= models.DateTimeField(_('publish'))
	created			= models.DateTimeField(_('created'), auto_now_add=True)
	modified		= models.DateTimeField(_('modified'), auto_now=True)
	                
	tags			= TagField()
	
	class Meta:
		verbose_name = _('snippet')
		verbose_name_plural = _('snippets')
		ordering = ('-publish',)
		get_latest_by = 'publish'
	
	class Admin:
		list_display = ('title', 'syntax', 'author', 'publish')
		list_filter = ('publish', 'author')
	
	def __unicode__(self):
		return u"%s: %s" % (self.syntax, self.title)
	
	def get_absolute_url(self):
		ctype = ContentType.objects.get(model='snippet', app_label='tumblelog')
		item = Item.objects.get(object_id=self.id, content_type=ctype)
		return item.get_absolute_url()

Snippet.save = save_as_item
Snippet.delete = delete_as_item