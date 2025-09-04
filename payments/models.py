from django.db import models
from django.core.validators import MinValueValidator
import uuid
from core.models import TimeStampedModel
from customers.models import Customer
from orders.models import Order


class PaymentMethod(TimeStampedModel):
    """
    Available payment methods (Stripe, PayPal, etc.)
    """
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=50)  # stripe, paypal, etc.
    is_active = models.BooleanField(default=True)
    
    # Configuration (stored as JSON or separate fields)
    config = models.JSONField(default=dict, blank=True)
    
    # Display settings
    display_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='payment_methods/', blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.display_name or self.name
    
    class Meta:
        db_table = 'payments_payment_method'
        ordering = ['sort_order', 'name']


class Payment(TimeStampedModel):
    """
    Payment transactions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]
    
    TRANSACTION_TYPES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('partial_refund', 'Partial Refund'),
    ]
    
    # Payment identification
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_id = models.CharField(max_length=255, unique=True, db_index=True)
    
    # Related objects
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='payment')
    
    # Gateway information
    gateway_transaction_id = models.CharField(max_length=255, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    gateway_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Processing details
    processed_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
    
    @property
    def is_successful(self):
        return self.status == 'completed'
    
    @property
    def can_be_refunded(self):
        return self.status == 'completed' and self.transaction_type == 'payment'
    
    class Meta:
        db_table = 'payments_payment'
        ordering = ['-created_at']


class Refund(TimeStampedModel):
    """
    Refund transactions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Refund identification
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    refund_id = models.CharField(max_length=255, unique=True, db_index=True)
    
    # Related objects
    original_payment = models.ForeignKey(Payment, related_name='refunds', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='refunds', on_delete=models.CASCADE)
    
    # Refund details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Gateway information
    gateway_refund_id = models.CharField(max_length=255, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Processing details
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Refund {self.refund_id} - ${self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.refund_id:
            self.refund_id = self.generate_refund_id()
        super().save(*args, **kwargs)
    
    def generate_refund_id(self):
        import random, string
        return 'REF-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    class Meta:
        db_table = 'payments_refund'
        ordering = ['-created_at']


class CustomerPaymentMethod(TimeStampedModel):
    """
    Saved payment methods for customers
    """
    customer = models.ForeignKey(Customer, related_name='saved_payment_methods', on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    
    # Tokenized payment info (never store sensitive data)
    gateway_customer_id = models.CharField(max_length=255)
    gateway_payment_method_id = models.CharField(max_length=255)
    
    # Display information
    display_name = models.CharField(max_length=100)  # e.g., "**** **** **** 1234"
    card_type = models.CharField(max_length=20, blank=True)  # visa, mastercard, etc.
    last_four_digits = models.CharField(max_length=4, blank=True)
    expiry_month = models.IntegerField(null=True, blank=True)
    expiry_year = models.IntegerField(null=True, blank=True)
    
    # Settings
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.customer.email} - {self.display_name}"
    
    @property
    def is_expired(self):
        if not (self.expiry_month and self.expiry_year):
            return False
        
        from datetime import date
        today = date.today()
        return (self.expiry_year < today.year or 
                (self.expiry_year == today.year and self.expiry_month < today.month))
    
    class Meta:
        db_table = 'payments_customer_payment_method'
        unique_together = ['customer', 'gateway_payment_method_id']


class PaymentWebhook(TimeStampedModel):
    """
    Payment gateway webhooks for tracking events
    """
    EVENT_TYPES = [
        ('payment.succeeded', 'Payment Succeeded'),
        ('payment.failed', 'Payment Failed'),
        ('refund.created', 'Refund Created'),
        ('customer.created', 'Customer Created'),
        ('customer.updated', 'Customer Updated'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
        ('ignored', 'Ignored'),
    ]
    
    # Webhook identification
    webhook_id = models.CharField(max_length=255, unique=True, db_index=True)
    provider = models.CharField(max_length=50)  # stripe, paypal, etc.
    event_type = models.CharField(max_length=50)
    
    # Webhook data
    data = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Processing details
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    attempts = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.provider} webhook: {self.event_type} - {self.status}"
    
    class Meta:
        db_table = 'payments_webhook'
        ordering = ['-created_at']
