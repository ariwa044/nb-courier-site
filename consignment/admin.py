from django.contrib import admin
from .models import Package


class PackageAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'package_name', 'mode_of_transit',
        'package_status','shipping_date', 'delivery_date', 'current_location', 'sender', 'receiver',
    )
    search_fields = ('package_id', 'package_name', 'tracking_code')
    list_filter = ('package_status', 'mode_of_transit', 'shipping_date')

    # Custom display for map iframes in the admin panel
    def map_iframe(self, obj):
        iframe_html = ''
        if obj.current_location:
            iframe_html += f'<iframe src="{obj.current_location}" width="100" height="100"></iframe>'
        return iframe_html or "No Map URLs Provided"

    map_iframe.short_description = 'Map Preview'
    map_iframe.allow_tags = True
    
admin.site.register(Package, PackageAdmin)
