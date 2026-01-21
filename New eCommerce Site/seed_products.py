import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User, SellerProfile
from apps.products.models import Product, ProductVariant

def seed():
    # 1. Create Seller
    email = 'seller@example.com'
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(email=email, password='password123', role=User.Role.SELLER, is_verified=True)
        SellerProfile.objects.create(user=user, business_name='TeknoStore', status=SellerProfile.Status.APPROVED)
        print(f"Created seller: {email}")
    else:
        user = User.objects.get(email=email)
        print(f"Using existing seller: {email}")

    # 2. Products to create
    products_data = [
        ("Akıllı Telefon 13", "En yeni özelliklerle donatılmış akıllı telefon.", 25000.00, "elektronik"),
        ("Kablosuz Kulaklık Pro", "Aktif gürültü engelleme özellikli.", 3500.00, "elektronik"),
        ("Laptop Pro X", "Yüksek performanslı iş bilgisayarı.", 45000.00, "elektronik"),
        ("Erkek T-Shirt", "Baskılı pamuklu t-shirt.", 250.00, "moda"),
        ("Spor Ayakkabı", "Rahat koşu ayakkabısı.", 1200.00, "moda"),
        ("Deri Ceket", "Hakiki deri siyah ceket.", 4500.00, "moda"),
        ("Kahve Makinesi", "Otomatik filtre kahve makinesi.", 1500.00, "ev-yasam"),
        ("Akıllı Saat", "Spor ve sağlık takibi.", 2500.00, "elektronik"),
    ]

    for name, desc, price, cat in products_data:
        if Product.objects.filter(name=name).exists():
            continue
            
        # Create Product
        from django.utils.text import slugify
        import uuid
        slug = f"{slugify(name)}-{uuid.uuid4().hex[:6]}"
        
        prod = Product.objects.create(
            seller=user,
            name=name,
            slug=slug,
            description=f"{desc} Bu harika bir ürün. Stoklarla sınırlı!",
            status=Product.Status.ACTIVE
        )
        
        # Create Variant (required for price)
        ProductVariant.objects.create(
            product=prod,
            sku=f"SKU-{uuid.uuid4().hex[:8].upper()}",
            name="Standart",
            price=price,
            stock_quantity=50
        )
        
        print(f"Created product: {name}")

    print("Seeding complete.")

if __name__ == '__main__':
    seed()
