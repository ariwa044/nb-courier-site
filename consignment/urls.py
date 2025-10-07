from django.urls import path
from . import views

app_name = 'track'

urlpatterns = [
    path('', views.track_package, name='track_package'),
    #path('track/', views.track_package, name='track_package'),
    path('package/<str:package_id>/', views.package_detail, name='package_detail'),
    path('receipt/<str:package_id>/', views.generate_pdf, name='generate_pdf'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('cookies-policy/', views.cookies_policy, name='cookies_policy'),
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
    path('returns-policy/', views.returns_policy, name='returns_policy'),
]
