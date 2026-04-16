from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cars.models import Car


def register(request):
    """Simple user registration"""
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/reister.html', {'form': form})


@login_required
def profile(request):
    """USer profile"""
    return render(request, 'accounts/profile.html')

@login_required
def saved_cars(request):
    """User saved cars"""
    saved_cars_id = request.session.get('saved_cars', [])
    saved_cars = Car.objects.filter(id__in=saved_cars_id)

    return render(request, 'accounts/saved_cars.html', {
        'saced_cars': saved_cars
    })