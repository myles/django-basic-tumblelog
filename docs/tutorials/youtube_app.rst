Example YouTube Application
===========================

model.py
********

::
	
	from django.db import models
	
	class YouTube(models.Model):
		title = models.CharField(max_length=200)
		body = models.TextField(blank=True, null=True)
		url = models.URLField()