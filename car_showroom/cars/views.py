from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from . models import Car, TestDrive, Inquiry, Make
from . forms import TestDriveForm, InquiryForm




class CarListView(ListView):
    """Main car listing page with filtering"""
    model = Car
    template_name = 'cars/list.html'
    paginate_by = 12
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = Car.objects.filter(is_sold=False).select_related('make')

        # Get filter parameters from request
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        make_id = self.request.GET.get('make_id')
        fuel_type = self.request.GET.get('fuel_type')
        transmission = self.request.GET.get('transmission')
        search_query = self.request.GET.get('q')

        # Apply filters
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if make_id:
            queryset = queryset.filter(make_id=make_id)
        if fuel_type:
            queryset = queryset.filter(fuel_type=fuel_type)
        if transmission:
            queryset = queryset.filter(transmission=transmission)
        if search_query:
            queryset = queryset.filter(
                Q(make__name__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['make'] = Make.objects.all()
        context['featured_cars'] = Car.objects.filter(is_featured=True, is_sold=False)[:3]
        return context


class CarDetailView(DetailView):
    """Single car detail page"""
    model = Car
    template_name = 'cars/detail.html'
    context_object_name = 'car'

    def get_queryset(self):
        return Car.objects.select_related('make')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['inquiry_form'] = InquiryForm(initial={'car': self.object})
        context['test_drive_form'] = TestDriveForm(initial={'car': self.object})

        # Get related cars
        related_cars = Car.objects.filter(
            make = self.object.make,
            is_sold = False
        ).exclude(id=self.object.id)[:4]
        context['related_cars'] = related_cars

        return context

def car_search(request):
    """Simple search functionality"""
    query = request.GET.get('q', '')
    if query:
        results = Car.objects.filter(
            Q(make__name__icontains=query) |
            Q(model__icontains=query) |
            Q(description__icontains=query)
        ).filter(is_sold=False).select_related('make')
    else:
        results = Car.objects.none()

    return render(request, 'cars/search_results.html', {
        'results': results,
        'query': query
    })                


def create_inquiry(request, car_id):
    """Handle car inquiry form submission"""
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.car = car
            inquiry.save()

            messages.success(request, 'Your inquiry has been submitted successfully! We will contact you soon')
            return redirect('car_detail', pk=car.id)
    else:
        form = InquiryForm()

    return render(request, 'cars/detail.html', {
        'car': car,
        'inquiry_form': form
    })        


def schedule_test_drive(request, car_id):
    """Handle test drive scheduling"""
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = TestDriveForm(request.POST)
        if form.is_valid():
            test_drive = form.save(commit=False)
            test_drive.car = car
            test_drive.save()

            messages.success(request, 'Test drive scheduled successfully! We will confirm your appointment.')
            return redirect('car_detail', pk=car.id)
    else:
        form = TestDriveForm()

    return render(request, 'cars/detail.html', {
        'car': car,
        'test_drive_form': form
    })       


class CarsByMakeView(ListView):
    """Show all cars by a specific make"""
    template_name = 'cars/by_make.html'
    context_object_name = 'cars'
    paginate_by = 12

    def get_queryset(self):
        self.make = get_object_or_404(Make, slug=self.kwargs['make_slug'])
        return Car.objects.filter(make=self.make, is_sold=False).select_related('make')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['make'] = self.make
        context['title'] = f'{self.make.name} Vehicles'
        return context
    

class FeaturedCarsView(ListView):
    """Show only featured cars"""
    template_name = 'cars/featured.html'
    context_object_name = 'cars'
    paginate_by = 12

    def get_queryset(self):
        return Car.objects.filter(is_featured=True, is_sold=False).select_related('make').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Featured Cars'
        context['description'] = 'Our handpicked selection of premimum vehicles'
        return context
    

class NewArrivalsView(ListView):
    """Show new cars added to inventory"""
    template_name = 'cars/new_arrivals.html'
    context_object_name = 'cars'
    paginate_by = 12
    
    def get_queryset(self):
        return Car.objects.filter(is_sold=False).order_by('-created_at').select_related('make')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Arrivals'
        context['description'] = 'Check out our latest additions to the inventory'
        return context