import datetime

from django.db.models import Manager

class PostManager(Manager):
	"""
	Managers for the Tumblelog Post model
	"""
	def __init__(self):
		super(TumblelogManager, self).__init__()
		self.models_by_name = {}
	
	def publisehd(self):
		return self.get_query_set().filter(
			published__lte=datetime.datetime.now()
		)
	
	def get_for_model(self, model):
		"""
		Return a QuerySet of only items of a certain type.
		"""
		return self.filter(
			content_type=ContentType.objects.get_for_model(model)
		)
	
	def get_last_update_of_model(self, model, **kwargs):
		"""
		Return the last time a given model's items were updated. Returns the
		epoch if the items were never updated.
		"""
		qs = self.get_for_model(model)
		if kwargs:
			qs = qs.filter(**kwargs)
		try:
			return qs.order_by('-publish')[0].published
		except IndexError:
			return datetime.fromtimestamp(0)