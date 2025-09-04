from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from core.models import TimeStampedModel


class Customer(AbstractUser, TimeStampedModel):
    """
    Extended user model for customers
    """
    phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Invalid phone number')]
    )
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Marketing preferences
    accepts_marketing = models.BooleanField(default=False)
    marketing_opt_in_date = models.DateTimeField(blank=True, null=True)
    
    # Account status
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    # Customer analytics
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def full_name(self):
        return self.get_full_name() or self.username
    
    class Meta:
        db_table = 'customers_customer'


class Address(TimeStampedModel):
    """
    Customer addresses
    """
    ADDRESS_TYPES = [
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    ]
    
    customer = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES)
    
    # Address fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=100, blank=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    
    # Settings
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_type_display()}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_address(self):
        parts = [
            f"{self.first_name} {self.last_name}",
            self.company,
            self.address_line_1,
            self.address_line_2,
            f"{self.city}, {self.state} {self.postal_code}",
            self.country
        ]
        return "\n".join([part for part in parts if part])
    
    class Meta:
        db_table = 'customers_address'
        verbose_name_plural = 'addresses'
