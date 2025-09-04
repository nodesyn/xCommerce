from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from core.models import TimeStampedModel, Category


class Product(TimeStampedModel):
    """
    Main product model
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('out_of_stock', 'Out of Stock'),
    ]
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True)
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Inventory
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    track_inventory = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    
    # Physical properties
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    length = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Length in cm")
    width = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Width in cm")
    height = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Height in cm")
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    requires_shipping = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product:detail', kwargs={'slug': self.slug})
    
    @property
    def is_in_stock(self):
        if not self.track_inventory:
            return True
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self):
        if not self.track_inventory:
            return False
        return self.stock_quantity <= self.low_stock_threshold
    
    @property
    def discount_percentage(self):
        if self.compare_at_price and self.compare_at_price > self.price:
            return int(((self.compare_at_price - self.price) / self.compare_at_price) * 100)
        return 0
    
    class Meta:
        db_table = 'products_product'
        ordering = ['-created_at']


class ProductImage(TimeStampedModel):
    """
    Product images
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product.name} - Image {self.sort_order}"
    
    class Meta:
        db_table = 'products_product_image'
        ordering = ['sort_order']


class ProductVariant(TimeStampedModel):
    """
    Product variants (size, color, etc.)
    """
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Pricing (can override product pricing)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Inventory
    stock_quantity = models.IntegerField(default=0)
    
    # Physical properties
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
    @property
    def effective_price(self):
        return self.price if self.price else self.product.price
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    class Meta:
        db_table = 'products_product_variant'


class ProductAttribute(TimeStampedModel):
    """
    Product attributes (color, size, material, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        db_table = 'products_attribute'


class ProductAttributeValue(TimeStampedModel):
    """
    Values for product attributes
    """
    attribute = models.ForeignKey(ProductAttribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    color_code = models.CharField(max_length=7, blank=True, null=True, help_text="Hex color code")
    
    def __str__(self):
        return f"{self.attribute.display_name}: {self.value}"
    
    class Meta:
        db_table = 'products_attribute_value'
        unique_together = ['attribute', 'value']


class ProductVariantAttribute(models.Model):
    """
    Link between product variants and their attribute values
    """
    variant = models.ForeignKey(ProductVariant, related_name='attributes', on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products_variant_attribute'
        unique_together = ['variant', 'attribute']
