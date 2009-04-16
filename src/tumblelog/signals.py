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

import datetime, logging

from django.contrib.contenttypes.models import ContentType

from tumblelog.models import Post

logger = logging.getLogger("tumblelog.signals")

def add_tumblelog_signal(sender, instance, user=None, publish=None, title=None **kwargs):
	ctype = ContentType.objects.get_for_model(instance)
	obj, created = Post.objects.get_or_create(content_type=ctype, object_id=instance.id)
	
	if user:
		obj.author = user
	
	if title:
		obj.title = title
	else:
		# TODO Add something to truncate after 200 characters.
		obj.title = instance.__unicode__()
	
	if publish:
		obj.publish = publish
	else:
		obj.publish = datetime.datetime.now()
	
	obj.save()

def delete_tumblelog_signal(sender, instance, **kwargs):
	ctype = ContentType.objects.get_for_model(instance)
	try:
		post = Post.objects.get(content_type=ctype, object_id=instance.id)
		post.delete()
	except Post.MultipleObjectsReturned:
		posts = Item.objects.filter(content_type=ctype, object_id=instance.id)
		# TODO Need to implement in case there are mutiple items in the Database.
	except Item.DoesNotExist:
		pass

def delete_tumblelog_childern_signal(sender, instance, **kwargs):
	instance.content_object.delete()