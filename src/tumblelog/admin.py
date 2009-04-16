from django.contrib import admin

from tumblelog.models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)
	date_hierarchy = 'published'

admin.site.register(Post, PostAdmin)