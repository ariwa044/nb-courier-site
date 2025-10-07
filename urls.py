from django.conf.urls import handler404, handler500
from django.urls import path
from . import views

urlpatterns = [
    # ... your url patterns here ...
]

handler404 = 'consignment.views.custom_404_view'
handler500 = 'consignment.views.custom_500_view'