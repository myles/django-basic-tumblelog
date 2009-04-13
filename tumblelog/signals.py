from django.contrib.contenttypes.models import ContentType
from tumblelog.models import Item

def add_tumblelog_signal(sender, instance, **kwargs):
	try:
		ctype = ContentType.objects.get_for_model(instance)
		item = Item.objects.get(content_type=ctype, object_id=instance.id)
		item.author = instance.author
		item.publish = instance.publish
		item.save()
	except Item.DoesNotExist:
		item = Item.objects.create(content_object=instance, author=instance.author, publish=instance.publish)

def delete_tumblelog_signal(sender, instance, **kwargs):
	ctype = ContentType.objects.get_for_model(instance)
	try:
		item = Item.objects.get(content_type=ctype, object_id=instance.id)
		item.delete()
	except Item.MultipleObjectsReturned:
		items = Item.objects.filter(content_type=ctype, object_id=instance.id)
		# TODO Need to implement in case there are mutiple items in the Database.
	except Item.DoesNotExist:
		pass

def delete_tumblelog_childern_signal(sender, instance, **kwargs):
	instance.content_object.delete()
