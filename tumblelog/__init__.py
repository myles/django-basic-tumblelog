# Signals

from django.db.models.signals import post_save, post_delete
from tumblelog.models import Link, Video, Twitter, Chat, Event, Photo, Audio, Quote, Snippet, Item
from tumblelog.signals import add_tumblelog_signal, delete_tumblelog_signal, delete_tumblelog_childern_signal

post_save.connect(add_tumblelog_signal, sender=Link)
post_save.connect(add_tumblelog_signal, sender=Video)
post_save.connect(add_tumblelog_signal, sender=Twitter)
post_save.connect(add_tumblelog_signal, sender=Chat)
post_save.connect(add_tumblelog_signal, sender=Event)
post_save.connect(add_tumblelog_signal, sender=Photo)
post_save.connect(add_tumblelog_signal, sender=Audio)
post_save.connect(add_tumblelog_signal, sender=Quote)
post_save.connect(add_tumblelog_signal, sender=Snippet)

post_delete.connect(delete_tumblelog_signal, sender=Link)
post_delete.connect(delete_tumblelog_signal, sender=Video)
post_delete.connect(delete_tumblelog_signal, sender=Twitter)
post_delete.connect(delete_tumblelog_signal, sender=Chat)
post_delete.connect(delete_tumblelog_signal, sender=Event)
post_delete.connect(delete_tumblelog_signal, sender=Photo)
post_delete.connect(delete_tumblelog_signal, sender=Audio)
post_delete.connect(delete_tumblelog_signal, sender=Quote)
post_delete.connect(delete_tumblelog_signal, sender=Snippet)

post_delete.connect(delete_tumblelog_childern_signal, sender=Item)