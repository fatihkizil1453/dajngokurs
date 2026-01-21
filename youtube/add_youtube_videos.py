import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_project.settings')
django.setup()

from django.contrib.auth.models import User
from videos.models import Video

def add_videos():
    # Ensure a uploader exists
    uploader, created = User.objects.get_or_create(username='youtube_admin')
    if created:
        uploader.set_password('admin123')
        uploader.save()

    sample_videos = [
        {
            "title": "Interstellar - Stay (Main Theme) - Hans Zimmer",
            "youtube_url": "https://www.youtube.com/embed/0S13mP_pfFY",
            "thumbnail_url": "https://img.youtube.com/vi/0S13mP_pfFY/maxresdefault.jpg",
            "description": "Powerful soundtrack from the movie Interstellar."
        },
        {
            "title": "Cyberpunk 2077 - Official Trailer",
            "youtube_url": "https://www.youtube.com/embed/8X2kIfS6fb8",
            "thumbnail_url": "https://img.youtube.com/vi/8X2kIfS6fb8/maxresdefault.jpg",
            "description": "Welcome to the future. Night City changes everything."
        },
        {
            "title": "Relaxing Nature Sounds - 4K Video",
            "youtube_url": "https://www.youtube.com/embed/668nUCeB73A",
            "thumbnail_url": "https://img.youtube.com/vi/668nUCeB73A/maxresdefault.jpg",
            "description": "Enjoy the calming sounds of birds and flowing water."
        },
        {
            "title": "SpaceX Starship Animation",
            "youtube_url": "https://www.youtube.com/embed/-Oox2w5sMcA",
            "thumbnail_url": "https://img.youtube.com/vi/-Oox2w5sMcA/maxresdefault.jpg",
            "description": "Animation of the Starship flight to Mars."
        },
        {
            "title": "Gordon Ramsay's Scrambled Eggs",
            "youtube_url": "https://www.youtube.com/embed/PUP7U5vTMM0",
            "thumbnail_url": "https://img.youtube.com/vi/PUP7U5vTMM0/maxresdefault.jpg",
            "description": "Learn to make the perfect scrambled eggs."
        },
        {
            "title": "MKBHD - iPhone 16 Review",
            "youtube_url": "https://www.youtube.com/embed/mK9B_x7C_3Y",
            "thumbnail_url": "https://img.youtube.com/vi/mK9B_x7C_3Y/maxresdefault.jpg",
            "description": "Is it worth the upgrade? Marques Brownlee investigates."
        },
        {
            "title": "MrBeast - I Spent 50 Hours In Solitary Confinement",
            "youtube_url": "https://www.youtube.com/embed/x9Q6D0EUMuA",
            "thumbnail_url": "https://img.youtube.com/vi/x9Q6D0EUMuA/maxresdefault.jpg",
            "description": "Can MrBeast survive the solitude?"
        },
        {
            "title": "The Weeknd - Blinding Lights (Official Video)",
            "youtube_url": "https://www.youtube.com/embed/4NRXx6U8ABQ",
            "thumbnail_url": "https://img.youtube.com/vi/4NRXx6U8ABQ/maxresdefault.jpg",
            "description": "Official music video for Blinding Lights."
        },
        {
            "title": "National Geographic - The Hidden World of Wolves",
            "youtube_url": "https://www.youtube.com/embed/Xm6_P58u6S0",
            "thumbnail_url": "https://img.youtube.com/vi/Xm6_P58u6S0/maxresdefault.jpg",
            "description": "Explore the life of the grey wolf."
        },
        {
            "title": "Veritasium - The Speed of Light",
            "youtube_url": "https://www.youtube.com/embed/msVuCEs8Ydo",
            "thumbnail_url": "https://img.youtube.com/vi/msVuCEs8Ydo/maxresdefault.jpg",
            "description": "Why the speed of light is so slow."
        },
        {
            "title": "Kurzgesagt - The Immune System Explained",
            "youtube_url": "https://www.youtube.com/embed/zQGOcOUBi6s",
            "thumbnail_url": "https://img.youtube.com/vi/zQGOcOUBi6s/maxresdefault.jpg",
            "description": "How your body fights for survival every day."
        },
        {
            "title": "Rick Astley - Never Gonna Give You Up",
            "youtube_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
            "description": "The classic RickRoll."
        },
        {
            "title": "LoFi Girl - Beats to relax/study to",
            "youtube_url": "https://www.youtube.com/embed/jfKfPfyJRdk",
            "thumbnail_url": "https://img.youtube.com/vi/jfKfPfyJRdk/maxresdefault.jpg",
            "description": "Infinite lofi beats."
        },
        {
            "title": "History of the World, I Guess",
            "youtube_url": "https://www.youtube.com/embed/xuCn8UX27wk",
            "thumbnail_url": "https://img.youtube.com/vi/xuCn8UX27wk/maxresdefault.jpg",
            "description": "Bill Wurtz explains history."
        },
        {
            "title": "NASA - We Are Going to the Moon",
            "youtube_url": "https://www.youtube.com/embed/0S6Bv_kM20M",
            "thumbnail_url": "https://img.youtube.com/vi/0S6Bv_kM20M/maxresdefault.jpg",
            "description": "Artemis mission update."
        }
    ]

    for v in sample_videos:
        if not Video.objects.filter(title=v['title']).exists():
            Video.objects.create(
                uploader=uploader,
                title=v['title'],
                youtube_url=v['youtube_url'],
                thumbnail_url=v['thumbnail_url'],
                description=v['description']
            )
            print(f"Added: {v['title']}")
        else:
            print(f"Skipped (Exists): {v['title']}")

if __name__ == "__main__":
    add_videos()
    print("15 YouTube videos added successfully")
