from django.urls import path
from . import views

app_name = 'estimator'

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listings, name='listings'),
    path('estimator/', views.estimator, name='estimator'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
