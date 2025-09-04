from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Abstract base model with created and updated timestamps
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Store(TimeStampedModel):
    """
    Store configuration and branding
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    domain = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='store/logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='store/favicons/', blank=True, null=True)
    
    # Contact information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Settings
    currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    is_active = models.BooleanField(default=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'core_store'


class Category(TimeStampedModel):
    """
    Product categories
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True
    )
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Display
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'core_category'
        verbose_name_plural = 'categories'
        ordering = ['sort_order', 'name']
