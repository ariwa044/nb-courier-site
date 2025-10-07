import random
import string
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
import socket
from smtplib import SMTPException

logger = logging.getLogger(__name__)

def send_package_email(package):
    """Send email notification with tracking information"""
    
    if not package.email:
        logger.warning(f"No email address provided for package {package.package_id}")
        return False

    subject = "Shipment Notification - Your Package is on the Way!"
    context = {
        'tracking_code': package.tracking_code,
        'destination': package.receiving_location,
        'current_location': package.current_location,
        'package': package
    }

    # Set socket timeout
    socket.setdefaulttimeout(30)  # 30 seconds timeout

    try:
        text_content = render_to_string('emails/package_notification.txt', context)
        html_content = render_to_string('emails/package_notification.html', context)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[package.email],
            fail_silently=False,
            html_message=html_content
        )
        logger.info(f"Email sent successfully for package {package.package_id}")
        return True
    except socket.timeout:
        logger.error(f"Connection timeout while sending email for package {package.package_id}")
        return False
    except SMTPException as smtp_error:
        logger.error(f"SMTP error while sending email for package {package.package_id}: {str(smtp_error)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while sending email for package {package.package_id}: {str(e)}")
        return False

def generate_tracking_code():
    # Start with 'CB' for Tracking
    start_letters = 'CE'
    # Generate random digits for middle section
    middle_digits = ''.join(random.choices(string.digits, k=14))
    
    tracking_code = f"{start_letters}{middle_digits}"
    
    # Check if tracking code already exists and regenerate if needed
    while Package.objects.filter(tracking_code=tracking_code).exists():
        middle_digits = ''.join(random.choices(string.digits, k=14))
        tracking_code = f"{start_letters}{middle_digits}"
    
    return tracking_code

def generate_package_id():
    # Start with 'EXP' for Package
    start_letters = 'EXP'
    # Generate random digits for middle section
    middle_digits = ''.join(random.choices(string.digits, k=4))
    
    package_id = f"{start_letters}_{middle_digits}"
    
    # Check if package ID already exists and regenerate if needed
    while Package.objects.filter(package_id=package_id).exists():
        middle_digits = ''.join(random.choices(string.digits, k=5))
        package_id = f"{start_letters}_{middle_digits}"
    
    return package_id

from datetime import date, timedelta

def default_delivery_date():
    return date.today() + timedelta(days=2)

def default_shipping_date():
    return date.today()
class Package(models.Model):
    tracking_code = models.CharField(
        max_length=32, 
        unique=True,
        default=generate_tracking_code,
        editable=True  # Makes it editable in admin
    )
    package_id = models.CharField(max_length=20, default=generate_package_id, unique=True)
    package_name = models.CharField(max_length=100)
    sender = models.CharField(max_length=100, null=True, blank=True)
    receiver = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=15, null=True, blank=True, help_text='receiver phone number')
    email = models.EmailField(max_length=100, null=True, blank=True, help_text='receiver email address')
    sending_location = models.CharField(max_length=100, null=True, blank=True, help_text='sender address & city')
    receiving_location = models.CharField(max_length=100, null=True, blank=True, help_text='receiver address & city')
    current_location = models.CharField(max_length=300, null=True, blank=True, help_text='name for map iframe')
    package_description = models.TextField(null=True, blank=True)



    MODE_OF_TRANSIT_CHOICES = [
        ('Air', 'Air'),
        ('Sea', 'Sea'),
        ('Road', 'Road')
    ]
    mode_of_transit = models.CharField(max_length=10, choices=MODE_OF_TRANSIT_CHOICES)

    PACKAGE_STATUS_CHOICES = [
        ('Shipment Processed', 'Shipment Processed'),
        ('In Transit', 'In Transit'),
        ('Awaiting Customs Clearance', 'Awaiting Customs Clearance'),
        ('Customs Cleared', 'Customs Cleared'),
        ('At Destination Facility', 'At Destination Facility'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
        ('Cancelled', 'Cancelled')
    ]
    package_status = models.CharField(max_length=32, choices=PACKAGE_STATUS_CHOICES)
    delivery_update = models.TextField(null=True, blank=True)
    #package_image = models.ImageField(upload_to='package_images/', default='default_image.jpg')
    package_weight = models.FloatField(null=True, blank=True, default=0.0)
    shipping_cost = models.FloatField(null=True, blank=True, default=0.0)
    package_quantity = models.IntegerField(default=1)

    shipping_date = models.DateField(default=default_shipping_date, null=True, blank=True)
    delivery_date = models.DateField(default=default_delivery_date, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Packages'

    def __str__(self):
        return f'{self.package_name} ({self.package_id}) '

@receiver(post_save, sender=Package)
def package_notification_handler(sender, instance, created, **kwargs):
    """Send email notification when a new package is created"""
    if created:
        send_package_email(instance)

# Connect the signal
post_save.connect(package_notification_handler, sender=Package)