# xCommerce Installation Guide

This guide will walk you through setting up xCommerce on your local development environment and preparing it for production deployment.

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **Database**: PostgreSQL 12+ (recommended) or SQLite for development
- **Cache**: Redis 6+ (optional but recommended)
- **Web Server**: Nginx or Apache (production only)
- **Memory**: Minimum 2GB RAM
- **Storage**: 10GB+ available space

### Development Tools
- **Git**: For version control
- **Node.js**: For frontend asset compilation (optional)
- **Docker**: For containerized deployment (optional)

## 🚀 Quick Installation

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/xcommerce.git
cd xcommerce

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit the .env file with your settings
nano .env
```

**Required .env settings:**
```bash
SECRET_KEY=your-super-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/xcommerce
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 4. Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see your xCommerce store!

## 🔧 Detailed Installation

### Database Configuration

#### PostgreSQL Setup (Recommended)

**Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# macOS with Homebrew
brew install postgresql

# Start PostgreSQL service
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS
```

**Create Database:**
```bash
sudo -u postgres psql

CREATE DATABASE xcommerce;
CREATE USER xcommerce_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE xcommerce TO xcommerce_user;
\q
```

**Update .env:**
```bash
DATABASE_URL=postgresql://xcommerce_user:your_password@localhost:5432/xcommerce
```

#### SQLite Setup (Development Only)

For quick development setup, SQLite works out of the box:
```bash
DATABASE_URL=sqlite:///db.sqlite3
```

### Redis Setup (Optional)

**Install Redis:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
sudo systemctl start redis  # Linux
brew services start redis   # macOS
```

**Update .env:**
```bash
REDIS_URL=redis://localhost:6379/0
```

### Email Configuration

**Gmail SMTP (Development):**
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**SendGrid (Production):**
```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

### Media Files Configuration

**Local Development:**
```bash
MEDIA_URL=/media/
MEDIA_ROOT=/path/to/xcommerce/media
```

**AWS S3 (Production):**
```bash
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

## 🐳 Docker Installation

### Using Docker Compose

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=1
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/xcommerce
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: xcommerce
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

volumes:
  postgres_data:
```

**Run with Docker:**
```bash
# Build and start containers
docker-compose up --build

# Run migrations (in another terminal)
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 🏗️ Development Setup

### IDE Configuration

**VS Code Settings (.vscode/settings.json):**
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

**PyCharm Configuration:**
1. File → Settings → Project → Python Interpreter
2. Select existing virtual environment: `./venv/bin/python`
3. Configure Django settings: `xcommerce.settings`

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
EOF
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test products

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## 🌍 Production Deployment

### Server Requirements

**Minimum Production Server:**
- 2 CPU cores
- 4GB RAM
- 50GB SSD storage
- Ubuntu 20.04 LTS or similar

### System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system packages
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git curl

# Install Python dependencies
sudo apt install -y python3-dev libpq-dev build-essential
```

### Application Deployment

**1. Clone and Setup:**
```bash
cd /opt
sudo git clone https://github.com/yourusername/xcommerce.git
sudo chown -R $USER:$USER xcommerce
cd xcommerce

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

**2. Environment Configuration:**
```bash
# Create production .env
cp .env.example .env

# Edit with production settings
nano .env
```

**Production .env:**
```bash
SECRET_KEY=your-very-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://xcommerce:password@localhost:5432/xcommerce
REDIS_URL=redis://localhost:6379/0
USE_S3=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

**3. Database and Static Files:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Web Server Configuration

**Gunicorn Service (/etc/systemd/system/xcommerce.service):**
```ini
[Unit]
Description=xCommerce Django Application
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/xcommerce
Environment=PATH=/opt/xcommerce/venv/bin
EnvironmentFile=/opt/xcommerce/.env
ExecStart=/opt/xcommerce/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    xcommerce.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration (/etc/nginx/sites-available/xcommerce):**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /opt/xcommerce/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /opt/xcommerce/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable and Start Services:**
```bash
# Enable services
sudo systemctl enable xcommerce
sudo systemctl enable nginx

# Start services
sudo systemctl start xcommerce
sudo systemctl start nginx

# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/xcommerce /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```

### SSL Certificate

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔍 Troubleshooting

### Common Issues

**Database Connection Error:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database exists
sudo -u postgres psql -l

# Test connection
python manage.py dbshell
```

**Static Files Not Loading:**
```bash
# Recollect static files
python manage.py collectstatic --clear

# Check STATIC_ROOT setting
python manage.py diffsettings | grep STATIC
```

**Permission Errors:**
```bash
# Fix file permissions
sudo chown -R www-data:www-data /opt/xcommerce/media
sudo chmod -R 755 /opt/xcommerce/static
```

**Memory Issues:**
```bash
# Check memory usage
free -h

# Check processes
ps aux | grep python

# Add swap if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Log Files

**Application Logs:**
```bash
# Django logs
tail -f /opt/xcommerce/logs/django.log

# Gunicorn logs
sudo journalctl -u xcommerce -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Health Checks

**System Health Script:**
```bash
#!/bin/bash
# health_check.sh

echo "=== System Health Check ==="

# Check services
echo "Services:"
sudo systemctl is-active postgresql
sudo systemctl is-active redis
sudo systemctl is-active nginx
sudo systemctl is-active xcommerce

# Check disk space
echo -e "\nDisk Usage:"
df -h /

# Check memory
echo -e "\nMemory Usage:"
free -h

# Check database connection
echo -e "\nDatabase Connection:"
cd /opt/xcommerce
source venv/bin/activate
python -c "
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
print('Database: OK')
"
```

## 📚 Next Steps

After successful installation:

1. **Configure your store** in Django Admin (`/admin/`)
2. **Customize the theme** following the [Customization Guide](customization.md)
3. **Add products** and categories
4. **Set up payment processing**
5. **Configure email templates**
6. **Test the complete purchase flow**

For additional help, see our [troubleshooting guide](troubleshooting.md) or [contact support](mailto:support@xcommerce.com).