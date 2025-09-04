from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product, ProductImage, ProductVariant, 
    ProductAttribute, ProductAttributeValue, ProductVariantAttribute
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'sort_order', 'is_primary']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ['name', 'sku', 'price', 'stock_quantity', 'is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'status', 'stock_quantity', 
        'is_featured', 'sales_count', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'requires_shipping', 'is_digital',
        'category', 'created_at'
    ]
    search_fields = ['name', 'description', 'sku']
    readonly_fields = ['created_at', 'updated_at', 'view_count', 'sales_count']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        ('Categorization', {
            'fields': ('category', 'categories')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_at_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': (
                'sku', 'barcode', 'track_inventory', 'stock_quantity', 
                'low_stock_threshold'
            ),
            'classes': ('collapse',)
        }),
        ('Physical Properties', {
            'fields': ('weight', 'length', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('Status & Visibility', {
            'fields': (
                'status', 'is_featured', 'requires_shipping', 'is_digital'
            )
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('view_count', 'sales_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'sort_order', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['created_at', 'updated_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'name', 'sku', 'effective_price', 'stock_quantity', 
        'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['product__name', 'name', 'sku']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'created_at']
    search_fields = ['name', 'display_name']
    readonly_fields = ['created_at', 'updated_at']


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value', 'color_preview', 'created_at']
    list_filter = ['attribute', 'created_at']
    search_fields = ['attribute__name', 'value']
    readonly_fields = ['created_at', 'updated_at']
    
    def color_preview(self, obj):
        if obj.color_code:
            return format_html(
                '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; display: inline-block;"></div>',
                obj.color_code
            )
        return "No Color"
    color_preview.short_description = "Color"
