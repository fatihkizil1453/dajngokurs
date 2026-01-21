from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/messaging/', include('apps.messaging.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/disputes/', include('apps.disputes.urls')),
    
    # Serve Static Frontend for Demo
    re_path(r'^site/(?P<path>.*)$', serve, {'document_root': str(settings.BASE_DIR / 'frontend')}),
    path('', RedirectView.as_view(url='/site/buyer/index.html', permanent=False)),
]

from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
