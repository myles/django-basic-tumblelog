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