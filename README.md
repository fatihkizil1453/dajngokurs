# Multi-Vendor E-Commerce Platform

## Architecture
- **Backend**: Django & Django REST Framework
- **Database**: SQLite (Dev) / PostgreSQL (Prod ready)
- **Auth**: Custom User Model (Email-based), Session + Token

## Apps
- `accounts`: Authentication & Profiles (Admin, Seller, Buyer)
- `products`: Catalog management, Variants, Bundles
- `orders`: Multi-vendor checkout, Stock management
- `messaging`: Order-based chat
- `disputes`: Refund/Return management
- `reviews`: Verified purchase reviews

## Setup
1. `python -m venv venv`
2. `venv\Scripts\activate`
3. `pip install -r requirements.txt` (or manually install django, djangorestframework, psycopg2-binary, django-cors-headers, Pillow)
4. `python manage.py migrate`
5. `python manage.py createsuperuser`
6. `python manage.py runserver`

## API Demo
See [API_DEMO_SCENARIOS.md](API_DEMO_SCENARIOS.md) for step-by-step usage.

## Testing
Run `python manage.py test apps.accounts apps.products apps.orders apps.disputes`
