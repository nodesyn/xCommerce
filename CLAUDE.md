# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a new Django e-commerce store project called "DjangoStore". The repository is currently minimal with only a single `prd.md` file present, indicating this is likely a greenfield project in its initial setup phase.

## Development Setup

Since this appears to be a new Django project, the typical development workflow will involve:

- Creating a Django project structure with `django-admin startproject`
- Setting up a virtual environment for Python dependencies
- Installing Django and related packages via pip
- Configuring database settings (likely SQLite for development)
- Creating Django apps for different store functionalities (products, orders, users, etc.)

## Expected Architecture

For a Django e-commerce store, the typical structure will include:

- **Core Django apps**: Products, Orders, Users/Authentication, Cart, Payment
- **Models**: Product, Category, Order, OrderItem, User profile extensions
- **Views**: Both function-based and class-based views for CRUD operations
- **Templates**: HTML templates for the store frontend
- **Static files**: CSS, JavaScript, and images
- **Admin interface**: Django admin customization for store management

## Common Commands

Once the Django project is set up, common commands will be:

- `python manage.py runserver` - Start development server
- `python manage.py migrate` - Apply database migrations  
- `python manage.py makemigrations` - Create new migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py collectstatic` - Collect static files for production
- `python manage.py test` - Run tests

## Notes

- The repository is not yet initialized as a Git repository
- No existing Django project structure is present
- Development dependencies and requirements files need to be created
- Database configuration will need to be set up based on deployment needs