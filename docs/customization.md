# xCommerce Customization & White Labeling Guide

This guide will help you customize xCommerce for your brand and create a unique shopping experience for your customers.

## 🎨 Visual Customization

### 1. Brand Colors and Theme

xCommerce uses CSS custom properties (variables) for easy theme customization. All colors are defined in `static/css/main.css`.

#### Primary Brand Colors

```css
:root {
  /* Primary Brand Colors - Main brand color used for buttons, links, etc. */
  --color-primary-50: #f0f9ff;   /* Very light tint */
  --color-primary-100: #e0f2fe;  /* Light tint */
  --color-primary-200: #bae6fd;  /* Medium light tint */
  --color-primary-300: #7dd3fc;  /* Medium tint */
  --color-primary-400: #38bdf8;  /* Medium */
  --color-primary-500: #0ea5e9;  /* Base brand color */
  --color-primary-600: #0284c7;  /* Medium dark */
  --color-primary-700: #0369a1;  /* Dark */
  --color-primary-800: #075985;  /* Darker */
  --color-primary-900: #0c4a6e;  /* Darkest */
}
```

#### Example Brand Customizations

**E-commerce Fashion Store**
```css
:root {
  /* Elegant pink/rose theme */
  --color-primary-50: #fdf2f8;
  --color-primary-100: #fce7f3;
  --color-primary-500: #ec4899;  /* Hot pink */
  --color-primary-600: #db2777;
  --color-primary-700: #be185d;
}
```

**Tech Store**
```css
:root {
  /* Modern purple theme */
  --color-primary-50: #faf5ff;
  --color-primary-100: #f3e8ff;
  --color-primary-500: #8b5cf6;  /* Purple */
  --color-primary-600: #7c3aed;
  --color-primary-700: #6d28d9;
}
```

**Organic/Natural Store**
```css
:root {
  /* Earth green theme */
  --color-primary-50: #f0fdf4;
  --color-primary-100: #dcfce7;
  --color-primary-500: #22c55e;  /* Green */
  --color-primary-600: #16a34a;
  --color-primary-700: #15803d;
}
```

#### Secondary Colors

```css
:root {
  /* Secondary colors for accents and highlights */
  --color-secondary-50: #f8fafc;
  --color-secondary-500: #64748b;
  --color-secondary-600: #475569;
  
  /* Status colors */
  --color-success-500: #10b981;  /* Success messages */
  --color-warning-500: #f59e0b;  /* Warnings */
  --color-error-500: #ef4444;    /* Errors */
}
```

### 2. Typography Customization

#### Font Selection

```css
:root {
  /* Google Fonts - add to base.html */
  --font-family-primary: 'Inter', system-ui, sans-serif;
  --font-family-heading: 'Playfair Display', serif;
  
  /* Font weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

#### Adding Custom Fonts

1. **Add Google Fonts to base.html:**
```html
<!-- In templates/base.html <head> section -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

2. **Update CSS variables:**
```css
:root {
  --font-family-primary: 'Inter', sans-serif;
  --font-family-heading: 'Playfair Display', serif;
}

/* Apply to specific elements */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-family-heading);
}
```

### 3. Logo and Branding

#### Setting Your Logo

1. **Via Django Admin:**
   - Go to `/admin/core/store/`
   - Upload your logo image
   - Set store name and description

2. **Direct Template Customization:**
```html
<!-- In templates/components/header.html -->
<a href="/" class="flex items-center space-x-2">
    <img src="{{ store.logo.url }}" alt="{{ store.name }}" class="h-10 w-auto">
    <span class="text-xl font-bold text-gray-900 dark:text-white">
        {{ store.name }}
    </span>
</a>
```

#### Logo Requirements
- **Format**: PNG, SVG (recommended), or JPG
- **Size**: Minimum 200x60px, maximum 800x240px
- **Aspect Ratio**: 3:1 or 4:1 works best
- **Background**: Transparent (PNG/SVG) preferred

### 4. Custom Styling Components

#### Button Styles

Customize button appearances in `static/css/main.css`:

```css
.btn-primary {
  @apply inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white;
  background: linear-gradient(135deg, var(--color-primary-500), var(--color-primary-600));
  transition: all 0.2s ease-in-out;
}

.btn-primary:hover {
  background: linear-gradient(135deg, var(--color-primary-600), var(--color-primary-700));
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
```

#### Card Styles

```css
.card {
  @apply bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700;
  transition: all 0.2s ease-in-out;
}

.card:hover {
  @apply shadow-lg;
  transform: translateY(-2px);
}
```

## 🏪 Store Configuration

### 1. Store Information

Configure your store details in Django Admin:

```python
# Access via /admin/core/store/
class Store(models.Model):
    name = "Your Store Name"
    description = "Your store description"
    logo = "path/to/your/logo.png"
    favicon = "path/to/favicon.ico"
    
    # Contact Information
    email = "contact@yourstore.com"
    phone = "+1 (555) 123-4567"
    address = "123 Main St, City, State 12345"
    
    # Social Media
    facebook_url = "https://facebook.com/yourstore"
    twitter_url = "https://twitter.com/yourstore"
    instagram_url = "https://instagram.com/yourstore"
    
    # SEO
    meta_description = "Your store's meta description for SEO"
    meta_keywords = "keyword1, keyword2, keyword3"
```

### 2. Homepage Customization

#### Hero Section

Edit `templates/store/home.html`:

```html
<!-- Hero Section -->
<section class="relative h-screen flex items-center justify-center overflow-hidden">
    <!-- Background Image/Video -->
    <div class="absolute inset-0 bg-cover bg-center" 
         style="background-image: url('{% static "images/hero-bg.jpg" %}');">
        <div class="absolute inset-0 bg-black bg-opacity-40"></div>
    </div>
    
    <!-- Hero Content -->
    <div class="relative z-10 text-center text-white max-w-4xl mx-auto px-6">
        <h1 class="text-5xl md:text-7xl font-bold mb-6">
            Your Amazing Store
        </h1>
        <p class="text-xl md:text-2xl mb-8 text-gray-200">
            Discover premium products with exceptional quality
        </p>
        <a href="{% url 'products:catalog' %}" class="btn-primary btn-lg">
            Shop Now
        </a>
    </div>
</section>
```

#### Featured Sections

Add custom sections:

```html
<!-- Value Propositions -->
<section class="py-16 bg-gray-50 dark:bg-gray-900">
    <div class="container mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="text-center">
                <div class="w-16 h-16 bg-primary-100 dark:bg-primary-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-primary-600"><!-- Icon --></svg>
                </div>
                <h3 class="text-xl font-semibold mb-2">Free Shipping</h3>
                <p class="text-gray-600 dark:text-gray-400">On orders over $50</p>
            </div>
            <!-- Repeat for other features -->
        </div>
    </div>
</section>
```

### 3. Navigation Customization

#### Main Navigation

Edit `templates/components/header.html`:

```html
<!-- Desktop Navigation -->
<nav class="hidden lg:flex lg:space-x-8">
    <a href="/" class="nav-link">Home</a>
    
    <!-- Products Dropdown -->
    <div class="relative group">
        <button class="nav-link flex items-center">
            Products
            <svg class="ml-1 w-4 h-4"><!-- Dropdown icon --></svg>
        </button>
        <div class="dropdown-menu">
            <a href="/products/category/electronics/">Electronics</a>
            <a href="/products/category/fashion/">Fashion</a>
            <a href="/products/category/home/">Home & Garden</a>
        </div>
    </div>
    
    <a href="/about/" class="nav-link">About</a>
    <a href="/contact/" class="nav-link">Contact</a>
</nav>
```

#### Footer Customization

Edit `templates/components/footer.html`:

```html
<footer class="bg-gray-900 text-white">
    <div class="container mx-auto px-6 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <!-- Company Info -->
            <div>
                <h3 class="text-lg font-semibold mb-4">{{ store.name }}</h3>
                <p class="text-gray-400 mb-4">{{ store.description }}</p>
                <div class="flex space-x-4">
                    <!-- Social Media Icons -->
                </div>
            </div>
            
            <!-- Quick Links -->
            <div>
                <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
                <ul class="space-y-2">
                    <li><a href="/about/" class="text-gray-400 hover:text-white">About Us</a></li>
                    <li><a href="/contact/" class="text-gray-400 hover:text-white">Contact</a></li>
                    <li><a href="/shipping/" class="text-gray-400 hover:text-white">Shipping Info</a></li>
                </ul>
            </div>
        </div>
    </div>
</footer>
```

## 🛍️ Product Customization

### 1. Product Display

#### Product Cards

Customize product card layout in `templates/products/catalog.html`:

```html
<div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden group hover:shadow-lg transition-shadow">
    <!-- Product Image -->
    <div class="aspect-square overflow-hidden">
        <img src="{{ product.images.first.image.url }}" 
             alt="{{ product.name }}"
             class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
    </div>
    
    <!-- Product Info -->
    <div class="p-4">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-2">
            {{ product.name }}
        </h3>
        <p class="text-gray-600 dark:text-gray-400 text-sm mb-3">
            {{ product.short_description|truncatechars:80 }}
        </p>
        
        <!-- Price and Actions -->
        <div class="flex items-center justify-between">
            <span class="text-lg font-bold text-primary-600">
                ${{ product.price }}
            </span>
            <button class="btn-primary btn-sm">Add to Cart</button>
        </div>
    </div>
</div>
```

### 2. Custom Product Fields

Add custom fields to products:

```python
# In products/models.py
class Product(TimeStampedModel):
    # ... existing fields ...
    
    # Custom fields
    brand = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    care_instructions = models.TextField(blank=True)
    size_chart = models.ImageField(upload_to='products/size_charts/', blank=True)
    video_url = models.URLField(blank=True)
```

## 🎭 Advanced Customization

### 1. Custom CSS Classes

Create reusable CSS classes:

```css
/* Custom component classes */
.product-badge {
    @apply absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full font-medium;
}

.price-tag {
    @apply text-2xl font-bold text-gray-900 dark:text-white;
}

.price-tag.sale {
    @apply text-red-600;
}

.price-original {
    @apply text-lg text-gray-500 line-through ml-2;
}

/* Animation utilities */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
```

### 2. JavaScript Customization

Add custom JavaScript functionality:

```javascript
// In static/js/custom.js

// Custom product interactions
document.addEventListener('DOMContentLoaded', function() {
    // Product image gallery
    initializeProductGallery();
    
    // Quick view modals
    initializeQuickView();
    
    // Custom animations
    initializeScrollAnimations();
});

function initializeProductGallery() {
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    const mainImage = document.querySelector('.product-main-image');
    
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            mainImage.src = this.dataset.fullImage;
        });
    });
}
```

### 3. Email Template Customization

Customize email templates in `templates/emails/`:

```html
<!-- templates/emails/order_confirmation.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Order Confirmation - {{ store.name }}</title>
    <style>
        /* Email-safe CSS */
        .container { max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }
        .header { background-color: {{ store.primary_color }}; color: white; padding: 20px; }
        .content { padding: 20px; }
        .footer { background-color: #f8f9fa; padding: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ store.name }}</h1>
            <h2>Order Confirmation</h2>
        </div>
        
        <div class="content">
            <p>Thank you for your order, {{ customer.first_name }}!</p>
            <p>Your order #{{ order.order_number }} has been confirmed.</p>
            
            <!-- Order details -->
            <table style="width: 100%; border-collapse: collapse;">
                <!-- Order items -->
            </table>
        </div>
        
        <div class="footer">
            <p>&copy; {{ current_year }} {{ store.name }}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
```

## 🌐 Multi-language Support

### 1. Django Internationalization

Enable multiple languages:

```python
# In settings.py
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

### 2. Template Translation

```html
{% load i18n %}

<h1>{% trans "Welcome to our store" %}</h1>
<button>{% trans "Add to Cart" %}</button>

<!-- For variables -->
{% blocktrans with name=product.name %}
    Product: {{ name }}
{% endblocktrans %}
```

## 🚀 Performance Optimization

### 1. Image Optimization

Configure image processing:

```python
# In settings.py
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'
THUMBNAIL_FORMAT = 'WEBP'
THUMBNAIL_QUALITY = 85

# Custom image processing
from PIL import Image
from django.core.files.storage import default_storage

def optimize_product_image(image_field):
    """Optimize product images for web display"""
    with Image.open(image_field) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        if img.width > 1200:
            ratio = 1200 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((1200, new_height), Image.LANCZOS)
        
        # Save optimized version
        img.save(image_field.path, 'JPEG', quality=85, optimize=True)
```

### 2. Caching Strategy

```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache timeout settings
CACHE_TTL = 60 * 60  # 1 hour

# In views
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')  # 15 minutes
class ProductCatalogView(ListView):
    model = Product
```

## 🔧 Advanced White Labeling

### 1. Multi-tenant Setup

For multiple stores from one installation:

```python
# In core/models.py
class Store(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    subdomain = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    theme_settings = models.JSONField(default=dict)
    
    def get_theme_css(self):
        """Generate CSS from theme settings"""
        css_vars = []
        for key, value in self.theme_settings.items():
            css_vars.append(f'--{key}: {value};')
        
        return ':root { ' + ' '.join(css_vars) + ' }'

# Middleware for multi-tenant
class MultiTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            store = Store.objects.get(domain=request.get_host())
            request.store = store
        except Store.DoesNotExist:
            request.store = Store.objects.get(is_default=True)
        
        return self.get_response(request)
```

### 2. Theme Management

```python
# Theme configuration system
class ThemeManager:
    def __init__(self, store):
        self.store = store
    
    def get_css_variables(self):
        """Get CSS variables for the current store's theme"""
        theme = self.store.theme_settings
        return {
            '--color-primary-500': theme.get('primary_color', '#0ea5e9'),
            '--color-secondary-500': theme.get('secondary_color', '#64748b'),
            '--font-family-primary': theme.get('font_family', 'Inter, sans-serif'),
            '--border-radius': theme.get('border_radius', '0.5rem'),
        }
    
    def generate_css(self):
        """Generate complete CSS for the theme"""
        variables = self.get_css_variables()
        css = ':root {\n'
        for key, value in variables.items():
            css += f'  {key}: {value};\n'
        css += '}\n'
        return css
```

This comprehensive customization guide covers all aspects of personalizing your xCommerce store. From simple color changes to advanced multi-tenant setups, you now have the tools to create a unique e-commerce experience that perfectly matches your brand.