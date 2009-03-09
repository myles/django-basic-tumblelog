from django.db.models import Manager

class ItemManager(Manager):
	
	def by_object(self, content_type_id):
		return self.get_query_set().filter(content_type=content_type_id)
