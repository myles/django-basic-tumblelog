Django Basic Apps
=================

`Django Basic Apps`_

.. _`Django Basic Apps`: http://code.google.com/p/django-basic-apps/

Blog
****

::

	from django.db.models.signals import post_save, post_delete
	
	from basic.blog.models import Post
	from tumblelog import signals
	
	def add_blog_post_tumblelog(sender, instance, **kwargs):
		if instance.status == 2:
			# This is just check to see if the blog post is Public.
			return signals.add_tumblelog_signal(sender, instance, **kwargs)
	
	post_save.connect(add_blog_post_tumblelog, sender=Post)
	
	def delete_blog_post_tumblelog(sender, instance, **kwargs):
		return signals.delete_tumblelog_signal(sender, instance, **kwargs)
	
	post_delete.connect(delete_blog_post_tumblelog, sender=Post)

Bookmarks
*********

::

	from django.db.models.signals import post_save, post_delete
	
	from basic.bookmarks.models import Bookmark
	from tumblelog import signals
	
	def add_bookmark_tumblelog(sender, instance, **kwargs):
		return signals.add_tumblelog_signal(sender, instance, publish_field='created', **kwargs)
	
	post_save.connect(add_bookmark_tumblelog, sender=Bookmark)
	
	def delete_bookmark_tumblelog(sender, instance, **kwargs):
		return signals.delete_tumblelog_signal(sender, instance, **kwargs)
	
	post_delete.connect(delete_bookmark_tumblelog, sender=Bookmark)

Media
*****

The Media application is split up into Audio, Photo, and Video.

Audio
-----

::

	from django.db.models.signals import post_save, post_delete
	
	from basic.media.models import Audio
	from tumblelog import signals
	
	def add_media_audio_tumblelog(sender, instance, **kwargs):
		return signals.add_tumblelog_signal(sender, instance, publish_field='uploaded', **kwargs)
	
	post_save.connect(add_media_audio_tumblelog, sender=Audio)
	
	post_delete.connect(signals.delete_tumblelog_signal, sender=Audio)

Photo
-----

::

	from django.db.models.signals import post_save, post_delete
	
	from basic.media.models import Photo
	from tumblelog import signals
	
	def add_media_photo_tumblelog(sender, instance, **kwargs):
		return signals.add_tumblelog_signal(sender, instance, publish_field='uploaded', **kwargs)
	
	post_save.connect(add_media_audio_tumblelog, sender=Photo)
	
	post_delete.connect(signals.delete_tumblelog_signal, sender=Photo)

Video
-----

::

	from django.db.models.signals import post_save, post_delete
	
	from basic.media.models import Video
	from tumblelog import signals
	
	def add_media_video_tumblelog(sender, instance, **kwargs):
		return signals.add_tumblelog_signal(sender, instance, publish_field='uploaded', **kwargs)
	
	post_save.connect(add_media_audio_tumblelog, sender=Video)
	
	post_delete.connect(signals.delete_tumblelog_signal, sender=Video)
