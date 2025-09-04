# xCommerce - Modern Django E-commerce Platform

[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.x-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, scalable, and customizable e-commerce platform built with Django. Features a beautiful responsive design, comprehensive product management, shopping cart functionality, customer accounts, and easy white-labeling capabilities.

## ✨ Features

### 🏪 **E-commerce Core**
- **Product Management**: Comprehensive product catalog with categories, variants, and attributes
- **Shopping Cart**: Full-featured cart with AJAX updates and session persistence
- **Checkout Process**: Streamlined checkout with multiple payment options
- **Order Management**: Complete order processing and tracking system
- **Inventory Control**: Stock management with low inventory alerts

### 👥 **Customer Experience**
- **User Authentication**: Custom registration and login system
- **Customer Accounts**: Personal dashboards with order history
- **Wishlist System**: Save products for later (authenticated users)
- **Address Management**: Multiple shipping/billing addresses
- **Order Tracking**: Real-time order status updates

### 🎨 **Modern Design**
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dark/Light Mode**: Built-in theme switching
- **Customizable Themes**: Easy rebranding with CSS variables
- **Interactive Components**: Alpine.js and HTMX for dynamic interactions
- **Professional UI**: Clean, modern interface design

### 🔧 **Technical Features**
- **Django 5.x**: Latest Django framework with best practices
- **PostgreSQL**: Robust database with full-text search
- **Redis**: Caching and session management
- **Celery**: Background task processing
- **Docker Ready**: Production deployment configuration
- **SEO Optimized**: Search engine friendly URLs and meta tags

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)
- Node.js (for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/xcommerce.git
   cd xcommerce
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to see your xCommerce store!

## 📁 Project Structure

```
xcommerce/
├── xcommerce/           # Main project settings
├── core/                # Core functionality and homepage
├── products/            # Product catalog and management
├── customers/           # User accounts and authentication
├── cart/                # Shopping cart and wishlist
├── orders/              # Order processing and management
├── payments/            # Payment processing integration
├── templates/           # HTML templates
│   ├── base.html
│   ├── components/      # Reusable UI components
│   ├── store/          # Store pages
│   ├── products/       # Product pages
│   ├── customers/      # Account pages
│   └── cart/           # Cart and checkout
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploaded files
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/xcommerce

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Email (for order notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Storage (for production)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

### Database Configuration

The project supports multiple database backends:

- **SQLite** (development): Default, no setup required
- **PostgreSQL** (recommended): Set `DATABASE_URL` in `.env`
- **MySQL**: Compatible with minor configuration changes

## 🎨 Customization & White Labeling

### Theme Customization

xCommerce uses CSS variables for easy theme customization. Edit `static/css/main.css`:

```css
:root {
  /* Primary Brand Colors */
  --color-primary-50: #f0f9ff;
  --color-primary-500: #0ea5e9;
  --color-primary-600: #0284c7;
  --color-primary-700: #0369a1;
  
  /* Secondary Colors */
  --color-secondary-500: #64748b;
  
  /* Success, Warning, Error */
  --color-success-500: #10b981;
  --color-warning-500: #f59e0b;
  --color-error-500: #ef4444;
  
  /* Typography */
  --font-family-primary: 'Inter', sans-serif;
  --font-family-heading: 'Inter', sans-serif;
  
  /* Spacing */
  --border-radius: 0.5rem;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
```

### Logo and Branding

1. **Logo**: Upload your logo in Django Admin → Core → Store
2. **Store Name**: Configure in Django Admin → Core → Store
3. **Favicon**: Set custom favicon in store settings
4. **Colors**: Update CSS variables as shown above
5. **Typography**: Change font families in CSS variables

### Store Configuration

Access Django Admin at `/admin/` to configure:

- **Store Settings**: Name, logo, description, contact info
- **Categories**: Product categories and navigation
- **Products**: Add/edit products, images, variants
- **Pages**: Create custom pages (About, Terms, etc.)
- **Email Templates**: Customize order confirmation emails

## 🚢 Deployment

### Using Docker

1. **Build the image**
   ```bash
   docker build -t xcommerce .
   ```

2. **Run with docker-compose**
   ```bash
   docker-compose up -d
   ```

### Manual Deployment

1. **Prepare for production**
   ```bash
   pip install gunicorn
   python manage.py collectstatic
   python manage.py migrate
   ```

2. **Configure web server** (Nginx example)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           alias /path/to/xcommerce/static/;
       }
       
       location /media/ {
           alias /path/to/xcommerce/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn xcommerce.wsgi:application --bind 0.0.0.0:8000
   ```

## 🔌 Integrations

### Payment Processors

xCommerce is designed to integrate with popular payment processors:

- **Stripe**: Credit cards, digital wallets
- **PayPal**: PayPal and credit card processing
- **Square**: In-person and online payments
- **Custom**: Build your own payment integration

### Shipping Providers

- **FedEx**: Real-time rates and tracking
- **UPS**: Shipping rates and label printing
- **USPS**: Postal service integration
- **Custom**: Add your preferred shipping provider

### Third-party Services

- **Google Analytics**: E-commerce tracking
- **Mailchimp**: Email marketing integration
- **Twilio**: SMS notifications
- **Cloudinary**: Advanced image processing

## 📊 Analytics & Monitoring

### Built-in Analytics

- Customer registration trends
- Product performance metrics
- Order completion rates
- Revenue reporting

### External Analytics

Configure Google Analytics 4 for advanced e-commerce tracking:

```html
<!-- Add to base.html template -->
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test products

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 API Documentation

xCommerce includes a REST API for mobile apps and integrations:

- **Products API**: `/api/products/`
- **Cart API**: `/api/cart/`
- **Orders API**: `/api/orders/`
- **Customers API**: `/api/customers/`

API documentation is available at `/api/docs/` when running the server.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Run linting
flake8 .
black .
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Customization Guide](docs/customization.md)
- [API Reference](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing](docs/contributing.md)

## 🐛 Troubleshooting

### Common Issues

**Database connection error**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify database exists
psql -U postgres -l
```

**Static files not loading**
```bash
# Collect static files
python manage.py collectstatic --clear

# Check STATIC_ROOT setting
```

**Cart not persisting**
```bash
# Check session configuration
python manage.py check --deploy
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋 Support

- **Documentation**: Check the [docs](docs/) folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/xcommerce/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/xcommerce/discussions)
- **Email**: support@yourcompany.com

## 🏆 Acknowledgments

- Django community for the amazing framework
- Tailwind CSS for the utility-first CSS framework
- Alpine.js for lightweight interactivity
- All contributors who helped build this platform

## 🗺️ Roadmap

- [ ] Multi-vendor marketplace support
- [ ] Advanced inventory management
- [ ] Subscription products
- [ ] Multi-language support
- [ ] Mobile app API
- [ ] Advanced analytics dashboard
- [ ] AI-powered product recommendations

---

**Made with ❤️ by the xCommerce team**

*Transform your business with a modern e-commerce platform that grows with you.*