from django.shortcuts import render
from django.http import JsonResponse
from .forms import EstimateForm
from .utils import estimate_price, estimate_with_location, average_estimates, format_try
import locale


def format_price(price):
    """Format price with commas for thousands separator"""
    try:
        # Set locale to Turkish for proper formatting
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        return locale.format_string("%d", price, grouping=True)
    except:
        # Fallback to simple comma insertion
        return f"{price:,}"


def home(request):
    # Sample property listings for the home page
    properties = [
        {
            'id': 1,
            'title': 'Modern 3+1 Apartment in Kadıköy',
            'price': 2500000,
            'formatted_price': format_price(2500000),
            'location': 'Kadıköy, Istanbul',
            'size': 120,
            'rooms': '3+1',
            'image': '/static/img/property1.svg',
            'description': 'Beautiful modern apartment with sea views, close to transportation.',
            'featured': True
        },
        {
            'id': 2,
            'title': 'Cozy 2+1 in Beşiktaş',
            'price': 1800000,
            'formatted_price': format_price(1800000),
            'location': 'Beşiktaş, Istanbul',
            'size': 85,
            'rooms': '2+1',
            'image': '/static/img/property2.svg',
            'description': 'Charming apartment in the heart of Beşiktaş, walking distance to shops.',
            'featured': True
        },
        {
            'id': 3,
            'title': 'Spacious 4+1 Villa in Ataşehir',
            'price': 3200000,
            'formatted_price': format_price(3200000),
            'location': 'Ataşehir, Istanbul',
            'size': 180,
            'rooms': '4+1',
            'image': '/static/img/property3.svg',
            'description': 'Luxurious villa with garden, perfect for families.',
            'featured': True
        },
        {
            'id': 4,
            'title': 'Studio Apartment in Şişli',
            'price': 950000,
            'formatted_price': format_price(950000),
            'location': 'Şişli, Istanbul',
            'size': 45,
            'rooms': '1+0',
            'image': '/static/img/property4.svg',
            'description': 'Compact and efficient studio perfect for young professionals.',
            'featured': False
        }
    ]

    context = {
        'properties': properties,
        'hero_title': 'Find Your Dream Home',
        'hero_subtitle': 'Discover the perfect property with our comprehensive listings and AI-powered price estimation tools.'
    }
    return render(request, 'estimator/home.html', context)


def listings(request):
    # More comprehensive property listings
    properties = [
        {
            'id': 1,
            'title': 'Modern 3+1 Apartment in Kadıköy',
            'price': 2500000,
            'formatted_price': format_price(2500000),
            'location': 'Kadıköy, Istanbul',
            'size': 120,
            'rooms': '3+1',
            'image': '/static/img/property1.svg',
            'description': 'Beautiful modern apartment with sea views, close to transportation. Features include modern kitchen, spacious living room, and balcony with Bosphorus views.',
            'bedrooms': 3,
            'bathrooms': 1,
            'floor': 5,
            'age': 2,
            'features': ['Sea View', 'Modern Kitchen', 'Balcony', 'Parking']
        },
        {
            'id': 2,
            'title': 'Cozy 2+1 in Beşiktaş',
            'price': 1800000,
            'formatted_price': format_price(1800000),
            'location': 'Beşiktaş, Istanbul',
            'size': 85,
            'rooms': '2+1',
            'image': '/static/img/property2.svg',
            'description': 'Charming apartment in the heart of Beşiktaş, walking distance to shops and restaurants. Recently renovated with modern amenities.',
            'bedrooms': 2,
            'bathrooms': 1,
            'floor': 3,
            'age': 8,
            'features': ['City Center', 'Renovated', 'Walking Distance to Shops']
        },
        {
            'id': 3,
            'title': 'Spacious 4+1 Villa in Ataşehir',
            'price': 3200000,
            'formatted_price': format_price(3200000),
            'location': 'Ataşehir, Istanbul',
            'size': 180,
            'rooms': '4+1',
            'image': '/static/img/property3.svg',
            'description': 'Luxurious villa with private garden, perfect for families. Includes garage, modern security system, and proximity to schools.',
            'bedrooms': 4,
            'bathrooms': 2,
            'floor': 2,
            'age': 1,
            'features': ['Garden', 'Garage', 'Security System', 'Family Friendly']
        },
        {
            'id': 4,
            'title': 'Studio Apartment in Şişli',
            'price': 950000,
            'formatted_price': format_price(950000),
            'location': 'Şişli, Istanbul',
            'size': 45,
            'rooms': '1+0',
            'image': '/static/img/property4.svg',
            'description': 'Compact and efficient studio perfect for young professionals. Fully furnished with modern appliances and city views.',
            'bedrooms': 1,
            'bathrooms': 1,
            'floor': 8,
            'age': 3,
            'features': ['Furnished', 'Modern Appliances', 'City Views']
        },
        {
            'id': 5,
            'title': 'Penthouse 4+2 in Üsküdar',
            'price': 4500000,
            'formatted_price': format_price(4500000),
            'location': 'Üsküdar, Istanbul',
            'size': 220,
            'rooms': '4+2',
            'image': '/static/img/property5.svg',
            'description': 'Exclusive penthouse with panoramic Bosphorus views. Features rooftop terrace, luxury finishes, and premium location.',
            'bedrooms': 4,
            'bathrooms': 2,
            'floor': 15,
            'age': 0,
            'features': ['Penthouse', 'Terrace', 'Bosphorus View', 'Luxury Finishes']
        },
        {
            'id': 6,
            'title': 'Traditional 3+1 in Beyoğlu',
            'price': 2100000,
            'formatted_price': format_price(2100000),
            'location': 'Beyoğlu, Istanbul',
            'size': 110,
            'rooms': '3+1',
            'image': '/static/img/property6.svg',
            'description': 'Historic building with modern updates. Located in the vibrant Beyoğlu district, close to cultural attractions and nightlife.',
            'bedrooms': 3,
            'bathrooms': 1,
            'floor': 4,
            'age': 25,
            'features': ['Historic Building', 'Cultural District', 'Modern Updates']
        }
    ]

    context = {'properties': properties}
    return render(request, 'estimator/listings.html', context)


def estimator(request):
    form = EstimateForm(request.POST or None)
    result = None

    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            base = estimate_price(
                square_meters=cd['square_meters'],
                rooms=cd['rooms'],
                floor=cd['floor'],
                age=cd['age'],
            )
            enhanced = estimate_with_location(
                square_meters=cd['square_meters'],
                rooms=cd['rooms'],
                floor=cd['floor'],
                age=cd['age'],
                location_rating=cd['location_rating'],
                transport=cd['transport'],
            )
            # we average the base and enhanced scores as requested
            result = average_estimates([base, enhanced])
        else:
            # form contains errors; they'll be displayed in template
            result = None

        # If this is an AJAX request return JSON response so the frontend can
        # update dynamically without a full page reload.
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid():
                return JsonResponse({'success': True, 'result': result, 'base': base, 'enhanced': enhanced})
            # convert form errors to a simple serializable dict
            errors_json = {}
            for field, errs in form.errors.get_json_data().items():
                errors_json[field] = [e.get('message') for e in errs]
            return JsonResponse({'success': False, 'errors': errors_json}, status=400)

    context = {'form': form, 'result': result}
    if result is not None and request.headers.get('x-requested-with') != 'XMLHttpRequest':
        # include preformatted Turkish Lira strings for server-rendered pages
        context['formatted_result'] = format_try(result)
        # include base/enhanced breakdown if available
        if 'base' in locals():
            context['formatted_base'] = format_try(base)
        if 'enhanced' in locals():
            context['formatted_enhanced'] = format_try(enhanced)

    return render(request, 'estimator/estimator.html', context)


def about(request):
    context = {
        'stats': {
            'properties': '10,000+',
            'cities': '81',
            'accuracy': '95%',
            'users': '50,000+'
        }
    }
    return render(request, 'estimator/about.html', context)


def contact(request):
    return render(request, 'estimator/contact.html')
