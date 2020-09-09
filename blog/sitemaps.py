from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import BlogPost

class StaticViewSitemap(Sitemap):
	def items(self):
		return ["home"]
	def location(self, items):
		return reverse(items)
class BlogPostSitemap(Sitemap):
	def items(self):
		changefreq = "hourly"
		priority = 0.5
		return BlogPost.objects.all()
	def lastmod(self, obj):
		return obj.date
