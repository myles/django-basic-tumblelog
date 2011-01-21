from django.conf import settings

TUMBLELOG_PAGINATE_BY = getattr(settings, 'TUMBLELOG_PAGINATE_BY', 20)