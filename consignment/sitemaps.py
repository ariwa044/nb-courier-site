from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Package

class PackageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Package.objects.all()

    def location(self, obj):
        return reverse('track:package_detail', kwargs={'package_id': obj.package_id})

    def lastmod(self, obj):
        pass  # Assuming you have an updated_at field

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['track:track_package']  # Add more static view names as needed

    def location(self, item):
        return reverse(item)