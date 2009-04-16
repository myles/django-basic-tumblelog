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

import datetime

from django.db.models import Manager

class PostManager(Manager):
	"""
	Managers for the Tumblelog Post model
	"""
	def __init__(self):
		super(PostManager, self).__init__()
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