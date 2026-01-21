from django.core.management.base import BaseCommand
from game.models import Word

class Command(BaseCommand):
    help = 'Seeds the database with initial Turkish words'

    def handle(self, *args, **kwargs):
        words = [
            # Şehirler
            ('ANKARA', 'Şehirler'),
            ('İSTANBUL', 'Şehirler'),
            ('İZMİR', 'Şehirler'),
            ('ANTALYA', 'Şehirler'),
            ('BURSA', 'Şehirler'),
            ('ADANA', 'Şehirler'),
            ('TRABZON', 'Şehirler'),
            ('ESKİŞEHİR', 'Şehirler'),
            # Meyve & Sebze
            ('ELMA', 'Meyve & Sebze'),
            ('ARMUT', 'Meyve & Sebze'),
            ('ÇİLEK', 'Meyve & Sebze'),
            ('KARPUZ', 'Meyve & Sebze'),
            ('KİRAZ', 'Meyve & Sebze'),
            ('PORTAKAL', 'Meyve & Sebze'),
            ('MANDALİNA', 'Meyve & Sebze'),
            ('ISPANAK', 'Meyve & Sebze'),
            # Hayvanlar
            ('ASLAN', 'Hayvanlar'),
            ('KAPLAN', 'Hayvanlar'),
            ('FİL', 'Hayvanlar'),
            ('ZÜRAFA', 'Hayvanlar'),
            ('KEDİ', 'Hayvanlar'),
            ('KÖPEK', 'Hayvanlar'),
            ('KURT', 'Hayvanlar'),
            ('AYI', 'Hayvanlar'),
            ('KARTAL', 'Hayvanlar'),
            # Teknoloji
            ('BİLGİSAYAR', 'Teknoloji'),
            ('YAZILIM', 'Teknoloji'),
            ('KLAVYE', 'Teknoloji'),
            ('EKRAN', 'Teknoloji'),
            ('TELEFON', 'Teknoloji'),
            ('İNTERNET', 'Teknoloji'),
        ]

        for text, category in words:
            word, created = Word.objects.get_or_create(text=text, category=category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {text}'))
            else:
                self.stdout.write(f'Skipped: {text}')
                
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(words)} words.'))
