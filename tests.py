__fixtures__ = ['tumblelog.json']
"""
>>> from django.test import Client
>>> from tumblelog.models import Link, Video, Chat

>>> link = Link.objects.get(pk=1)
>>> video = Video.objects.get(pk=1)
>>> chat = Chat.objects.get(pk=1)

>>> c = Client()

>>> r = c.get('/tumblelog/')
>>> r.status_code
200

>>> r = c.get('/tumblelog/link/1/')
>>> r.status_code
200

>>> r = c.get('/tumblelog/chat/1/')
>>> r.status_code
200

>>> r = c.get('/tumblelog/video/1/')
>>> r.status_code
200

"""