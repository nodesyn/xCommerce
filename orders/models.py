from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from core.models import TimeStampedModel
from customers.models import Customer, Address
from products.models import Product, ProductVariant


class Order(TimeStampedModel):
    """
    Order model
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
        ('failed', 'Failed'),
    ]
    
    # Order identification
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Customer information
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Addresses
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='billing_orders')
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='shipping_orders')
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order details
    currency = models.CharField(max_length=3, default='USD')
    notes = models.TextField(blank=True)
    
    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True)
    tracking_url = models.URLField(blank=True)
    
    # Fulfillment
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        import random, string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    @property
    def is_paid(self):
        return self.payment_status == 'paid'
    
    @property
    def can_be_cancelled(self):
        return self.status in ['pending', 'confirmed'] and not self.is_paid
    
    class Meta:
        db_table = 'orders_order'
        ordering = ['-created_at']


class OrderItem(TimeStampedModel):
    """
    Items within an order
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    
    # Product info at time of order (for historical accuracy)
    product_name = models.CharField(max_length=255)
    variant_name = models.CharField(max_length=255, blank=True)
    product_sku = models.CharField(max_length=100, blank=True)
    
    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'orders_order_item'


class OrderStatusHistory(TimeStampedModel):
    """
    Track order status changes
    """
    order = models.ForeignKey(Order, related_name='status_history', on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    changed_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Order {self.order.order_number}: {self.previous_status} → {self.new_status}"
    
    class Meta:
        db_table = 'orders_status_history'
        ordering = ['-created_at']


class Coupon(TimeStampedModel):
    """
    Discount coupons
    """
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    
    # Discount settings
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Usage limits
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Leave empty for unlimited")
    usage_count = models.PositiveIntegerField(default=0)
    usage_limit_per_customer = models.PositiveIntegerField(null=True, blank=True)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code
    
    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False
            
        if self.valid_from > now:
            return False
            
        if self.valid_until and self.valid_until < now:
            return False
            
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False
            
        return True
    
    def calculate_discount(self, amount):
        if not self.is_valid or amount < self.minimum_amount:
            return Decimal('0')
        
        if self.discount_type == 'percentage':
            discount = amount * (self.discount_value / 100)
        else:
            discount = self.discount_value
        
        if self.maximum_discount:
            discount = min(discount, self.maximum_discount)
            
        return min(discount, amount)
    
    class Meta:
        db_table = 'orders_coupon'


class OrderCoupon(models.Model):
    """
    Link between orders and applied coupons
    """
    order = models.ForeignKey(Order, related_name='applied_coupons', on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'orders_order_coupon'
        unique_together = ['order', 'coupon']
