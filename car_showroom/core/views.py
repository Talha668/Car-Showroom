from django.shortcuts import render
from cars.models import Car, Make
from django.core.paginator import Paginator


def home(request):
    """Homepage"""
    featured_cars = Car.objects.filter(is_featured=True, is_sold=False)[:6]
    new_arrivals = Car.objects.filter(is_sold=False).order_by('-created_at')[:6]

    return render(request, 'core/home.html', {
        'featured_cars': featured_cars,
        'new_arrivals': new_arrivals,
    })


def about(request):
    """About page"""
    return render(request, 'core/about.html')

def contact(Request):
    """Contact page"""
    return render(Request, 'core/contact.html')

def privacy(request):
    """Privacy policy page"""
    return render(request, 'core/privacy.html')

def terms(request):
    """Terms of service page"""
    return render(request, 'core/terms.html')