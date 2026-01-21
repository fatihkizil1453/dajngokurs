from django.core.management.base import BaseCommand
from apps.products.models import Category


class Command(BaseCommand):
    help = 'Delete auto-created categories, keeping only user-created ones'

    def handle(self, *args, **options):
        # List of categories that were auto-created by the script
        auto_created_slugs = [
            'moda',
            'ev-yasam', 
            'kozmetik',
            'spor-outdoor',
            'kitap-hobi',
            'oyuncak',
            'otomotiv',
        ]
        
        deleted_count = 0
        for slug in auto_created_slugs:
            try:
                category = Category.objects.get(slug=slug)
                category_name = category.name
                category.delete()
                deleted_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Deleted: {category_name}'))
            except Category.DoesNotExist:
                self.stdout.write(f'- Not found: {slug}')
        
        self.stdout.write(self.style.SUCCESS(f'\n{deleted_count} auto-created categories deleted.'))
        self.stdout.write(f'Remaining categories: {Category.objects.count()}')
        
        # Show remaining categories
        self.stdout.write('\nYour categories in admin panel:')
        for cat in Category.objects.all().order_by('order', 'name'):
            self.stdout.write(f'  - {cat.name} (slug: {cat.slug})')
