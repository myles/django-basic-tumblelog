from django.contrib.sitemaps import Sitemap

from tumblelog.models import Post

class TumblelogSitemap(Sitemap):
	changefreq = "never"
	priority = 0.5
	
	def items(self):
		return Post.objects.all()
	
	def lastmod(self, obj):
		return obj.publish