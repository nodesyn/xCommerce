# xCommerce API Reference

xCommerce provides a comprehensive REST API for mobile applications, third-party integrations, and headless commerce implementations.

## 🚀 Getting Started

### Base URL
```
https://your-store.com/api/v1/
```

### Authentication

xCommerce supports multiple authentication methods:

**1. Session Authentication (Web)**
```javascript
// Login first
fetch('/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        username: 'user@example.com',
        password: 'password'
    })
});
```

**2. Token Authentication (Mobile/API)**
```javascript
// Get token
const response = await fetch('/api/auth/token/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'user@example.com',
        password: 'password'
    })
});

const { token } = await response.json();

// Use token in subsequent requests
fetch('/api/products/', {
    headers: {
        'Authorization': `Token ${token}`
    }
});
```

**3. JWT Authentication (Advanced)**
```javascript
// Get JWT tokens
const response = await fetch('/api/auth/jwt/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'user@example.com',
        password: 'password'
    })
});

const { access, refresh } = await response.json();

// Use access token
fetch('/api/products/', {
    headers: {
        'Authorization': `Bearer ${access}`
    }
});
```

## 📦 Products API

### List Products
```http
GET /api/products/
```

**Parameters:**
- `category` (string): Filter by category slug
- `search` (string): Search in product name and description
- `min_price` (decimal): Minimum price filter
- `max_price` (decimal): Maximum price filter
- `in_stock` (boolean): Filter by stock availability
- `featured` (boolean): Filter featured products
- `ordering` (string): Sort by field (`name`, `price`, `-created_at`, etc.)
- `page` (integer): Page number for pagination
- `page_size` (integer): Results per page (max 100)

**Example Request:**
```javascript
const products = await fetch('/api/products/?category=electronics&min_price=10&max_price=1000&page=1&page_size=20');
```

**Response:**
```json
{
    "count": 150,
    "next": "https://your-store.com/api/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Premium Headphones",
            "slug": "premium-headphones",
            "description": "High-quality wireless headphones",
            "short_description": "Wireless headphones with noise cancellation",
            "price": "299.99",
            "compare_at_price": "399.99",
            "sku": "HEADPHONES-001",
            "status": "active",
            "is_featured": true,
            "is_in_stock": true,
            "stock_quantity": 25,
            "category": {
                "id": 1,
                "name": "Electronics",
                "slug": "electronics"
            },
            "images": [
                {
                    "id": 1,
                    "image": "https://your-store.com/media/products/headphones-1.jpg",
                    "alt_text": "Premium Headphones Front View",
                    "sort_order": 0
                }
            ],
            "variants": [
                {
                    "id": 1,
                    "name": "Black",
                    "price": "299.99",
                    "sku": "HEADPHONES-001-BLK",
                    "is_active": true,
                    "is_in_stock": true,
                    "stock_quantity": 15
                }
            ],
            "attributes": [
                {
                    "name": "Color",
                    "value": "Black"
                },
                {
                    "name": "Battery Life",
                    "value": "30 hours"
                }
            ],
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-20T14:45:00Z"
        }
    ]
}
```

### Get Product Details
```http
GET /api/products/{id}/
GET /api/products/{slug}/
```

**Response:**
```json
{
    "id": 1,
    "name": "Premium Headphones",
    "slug": "premium-headphones",
    "description": "Detailed product description...",
    "short_description": "Brief description",
    "price": "299.99",
    "compare_at_price": "399.99",
    "sku": "HEADPHONES-001",
    "status": "active",
    "is_featured": true,
    "is_in_stock": true,
    "stock_quantity": 25,
    "weight": "0.5",
    "dimensions": "20x15x8 cm",
    "category": {
        "id": 1,
        "name": "Electronics",
        "slug": "electronics",
        "description": "Electronic devices and accessories"
    },
    "images": [...],
    "variants": [...],
    "attributes": [...],
    "related_products": [...],
    "reviews": {
        "count": 45,
        "average_rating": 4.5,
        "ratings_breakdown": {
            "5": 25,
            "4": 12,
            "3": 5,
            "2": 2,
            "1": 1
        }
    },
    "seo": {
        "meta_title": "Premium Headphones - Best Sound Quality",
        "meta_description": "Experience premium sound with our wireless headphones...",
        "meta_keywords": "headphones, wireless, premium, audio"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:45:00Z"
}
```

## 📂 Categories API

### List Categories
```http
GET /api/categories/
```

**Response:**
```json
{
    "results": [
        {
            "id": 1,
            "name": "Electronics",
            "slug": "electronics",
            "description": "Electronic devices and accessories",
            "image": "https://your-store.com/media/categories/electronics.jpg",
            "parent": null,
            "children": [
                {
                    "id": 2,
                    "name": "Audio",
                    "slug": "audio",
                    "product_count": 25
                }
            ],
            "product_count": 150,
            "is_active": true,
            "sort_order": 1,
            "seo": {
                "meta_title": "Electronics - Latest Gadgets",
                "meta_description": "Discover the latest electronic devices..."
            }
        }
    ]
}
```

### Get Category Details
```http
GET /api/categories/{id}/
GET /api/categories/{slug}/
```

## 🛒 Cart API

### Get Cart
```http
GET /api/cart/
```

**Response:**
```json
{
    "id": "abc123",
    "items": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "name": "Premium Headphones",
                "price": "299.99",
                "image": "https://your-store.com/media/products/headphones-1.jpg"
            },
            "variant": {
                "id": 1,
                "name": "Black",
                "price": "299.99"
            },
            "quantity": 2,
            "unit_price": "299.99",
            "total_price": "599.98"
        }
    ],
    "subtotal": "599.98",
    "tax_amount": "47.99",
    "shipping_cost": "9.99",
    "total": "657.96",
    "item_count": 2,
    "created_at": "2024-01-20T10:00:00Z",
    "updated_at": "2024-01-20T10:30:00Z"
}
```

### Add to Cart
```http
POST /api/cart/items/
```

**Request Body:**
```json
{
    "product_id": 1,
    "variant_id": 1,
    "quantity": 2
}
```

**Response:**
```json
{
    "success": true,
    "message": "Item added to cart",
    "item": {
        "id": 1,
        "product": {...},
        "quantity": 2,
        "total_price": "599.98"
    },
    "cart": {
        "item_count": 3,
        "subtotal": "899.97"
    }
}
```

### Update Cart Item
```http
PUT /api/cart/items/{item_id}/
PATCH /api/cart/items/{item_id}/
```

**Request Body:**
```json
{
    "quantity": 3
}
```

### Remove from Cart
```http
DELETE /api/cart/items/{item_id}/
```

### Clear Cart
```http
DELETE /api/cart/
```

## 💝 Wishlist API

### Get Wishlist
```http
GET /api/wishlist/
```
*Requires authentication*

**Response:**
```json
{
    "items": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "name": "Premium Headphones",
                "price": "299.99",
                "image": "https://your-store.com/media/products/headphones-1.jpg",
                "is_in_stock": true
            },
            "added_at": "2024-01-20T10:00:00Z"
        }
    ],
    "item_count": 1
}
```

### Add to Wishlist
```http
POST /api/wishlist/items/
```

**Request Body:**
```json
{
    "product_id": 1
}
```

### Remove from Wishlist
```http
DELETE /api/wishlist/items/{item_id}/
```

## 📋 Orders API

### List Orders
```http
GET /api/orders/
```
*Requires authentication*

**Parameters:**
- `status` (string): Filter by order status
- `date_from` (date): Orders from date (YYYY-MM-DD)
- `date_to` (date): Orders to date (YYYY-MM-DD)

**Response:**
```json
{
    "count": 25,
    "results": [
        {
            "id": 1,
            "order_number": "ORD-2024-001",
            "status": "completed",
            "total_amount": "657.96",
            "item_count": 2,
            "created_at": "2024-01-20T10:00:00Z",
            "shipped_at": "2024-01-21T14:00:00Z",
            "delivered_at": "2024-01-23T16:30:00Z",
            "tracking_number": "1Z999AA1234567890"
        }
    ]
}
```

### Get Order Details
```http
GET /api/orders/{id}/
```

**Response:**
```json
{
    "id": 1,
    "order_number": "ORD-2024-001",
    "status": "completed",
    "items": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "name": "Premium Headphones",
                "image": "https://your-store.com/media/products/headphones-1.jpg"
            },
            "variant": {
                "id": 1,
                "name": "Black"
            },
            "quantity": 2,
            "unit_price": "299.99",
            "total_price": "599.98"
        }
    ],
    "billing_address": {
        "first_name": "John",
        "last_name": "Doe",
        "address_line_1": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "US"
    },
    "shipping_address": {...},
    "subtotal": "599.98",
    "tax_amount": "47.99",
    "shipping_cost": "9.99",
    "total_amount": "657.96",
    "payment_status": "paid",
    "payment_method": "credit_card",
    "tracking_number": "1Z999AA1234567890",
    "notes": "Please deliver to front door",
    "created_at": "2024-01-20T10:00:00Z",
    "updated_at": "2024-01-23T16:30:00Z"
}
```

### Create Order (Checkout)
```http
POST /api/checkout/
```

**Request Body:**
```json
{
    "billing_address": {
        "first_name": "John",
        "last_name": "Doe",
        "address_line_1": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "US",
        "phone": "+1 555-123-4567"
    },
    "shipping_address": {
        "first_name": "John",
        "last_name": "Doe",
        "address_line_1": "456 Oak Ave",
        "city": "New York",
        "state": "NY",
        "postal_code": "10002",
        "country": "US",
        "phone": "+1 555-123-4567"
    },
    "payment": {
        "method": "credit_card",
        "token": "tok_1234567890",
        "save_payment_method": false
    },
    "shipping_method": "standard",
    "notes": "Please deliver to front door"
}
```

**Response:**
```json
{
    "success": true,
    "order": {
        "id": 1,
        "order_number": "ORD-2024-001",
        "status": "processing",
        "total_amount": "657.96",
        "payment_status": "paid"
    },
    "payment": {
        "id": "pi_1234567890",
        "status": "succeeded",
        "amount": "657.96"
    }
}
```

## 👤 Customer API

### Customer Profile
```http
GET /api/account/profile/
```
*Requires authentication*

**Response:**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1 555-123-4567",
    "date_of_birth": "1990-01-15",
    "accepts_marketing": true,
    "date_joined": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-20T10:00:00Z"
}
```

### Update Profile
```http
PUT /api/account/profile/
PATCH /api/account/profile/
```

### Customer Addresses
```http
GET /api/account/addresses/
POST /api/account/addresses/
PUT /api/account/addresses/{id}/
DELETE /api/account/addresses/{id}/
```

## 🔍 Search API

### Product Search
```http
GET /api/search/products/
```

**Parameters:**
- `q` (string): Search query
- `category` (string): Category slug
- `filters` (object): Advanced filters

**Example:**
```javascript
const results = await fetch('/api/search/products/?q=headphones&category=electronics&filters={"brand":"sony","price_range":[100,500]}');
```

### Search Suggestions
```http
GET /api/search/suggestions/
```

**Parameters:**
- `q` (string): Partial search query

**Response:**
```json
{
    "suggestions": [
        "headphones",
        "headphones wireless",
        "headphones bluetooth"
    ],
    "products": [
        {
            "id": 1,
            "name": "Premium Headphones",
            "price": "299.99",
            "image": "..."
        }
    ]
}
```

## 📊 Analytics API

### Product Analytics
```http
GET /api/analytics/products/
```
*Requires admin authentication*

**Response:**
```json
{
    "top_products": [
        {
            "product": {
                "id": 1,
                "name": "Premium Headphones"
            },
            "total_sales": 150,
            "revenue": "44998.50"
        }
    ],
    "category_performance": [...],
    "recent_trends": [...]
}
```

## 🚨 Error Handling

### Error Response Format
```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "email": ["This field is required."],
            "password": ["Password must be at least 8 characters."]
        }
    }
}
```

### Common Error Codes

- `400` - Bad Request
  - `VALIDATION_ERROR` - Invalid input data
  - `INVALID_QUANTITY` - Invalid product quantity
  - `OUT_OF_STOCK` - Product out of stock

- `401` - Unauthorized
  - `AUTHENTICATION_REQUIRED` - Login required
  - `INVALID_CREDENTIALS` - Wrong username/password

- `403` - Forbidden
  - `PERMISSION_DENIED` - Insufficient permissions
  - `ACCOUNT_DISABLED` - Account is disabled

- `404` - Not Found
  - `PRODUCT_NOT_FOUND` - Product doesn't exist
  - `ORDER_NOT_FOUND` - Order doesn't exist

- `429` - Too Many Requests
  - `RATE_LIMIT_EXCEEDED` - API rate limit exceeded

- `500` - Internal Server Error
  - `SERVER_ERROR` - Unexpected server error

## 📝 Rate Limiting

API endpoints are rate limited to prevent abuse:

- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour
- **Premium accounts**: 10000 requests/hour

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 🔒 Webhooks

xCommerce can send webhooks for various events:

### Available Events
- `order.created` - New order placed
- `order.paid` - Order payment confirmed
- `order.shipped` - Order shipped
- `order.delivered` - Order delivered
- `product.created` - New product added
- `customer.registered` - New customer registered

### Webhook Payload Example
```json
{
    "event": "order.paid",
    "data": {
        "order": {
            "id": 1,
            "order_number": "ORD-2024-001",
            "total_amount": "657.96",
            "customer": {
                "id": 1,
                "email": "john@example.com"
            }
        }
    },
    "created_at": "2024-01-20T10:00:00Z"
}
```

### Webhook Security
Webhooks are signed with HMAC-SHA256. Verify signatures:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)
```

## 📚 SDK Libraries

### JavaScript/Node.js
```javascript
npm install @xcommerce/js-sdk

import XCommerce from '@xcommerce/js-sdk';

const client = new XCommerce({
    apiUrl: 'https://your-store.com/api/v1/',
    token: 'your-api-token'
});

// Get products
const products = await client.products.list({
    category: 'electronics',
    page: 1
});

// Add to cart
const cartItem = await client.cart.add({
    productId: 1,
    quantity: 2
});
```

### Python
```python
pip install xcommerce-python

from xcommerce import XCommerceAPI

client = XCommerceAPI(
    api_url='https://your-store.com/api/v1/',
    token='your-api-token'
)

# Get products
products = client.products.list(category='electronics')

# Add to cart
cart_item = client.cart.add(product_id=1, quantity=2)
```

This API reference covers the core functionality of xCommerce. For additional endpoints or custom implementations, please refer to the API documentation at `/api/docs/` when running your xCommerce instance.