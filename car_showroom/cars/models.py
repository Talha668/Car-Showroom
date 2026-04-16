from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User




class Make(models.Model):
    """Car Manufacturer"""
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='make/logo', blank=True, null=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.save()

    def get_absolute_urls(self):
        return reverse('cars_by_make', args=[self.slug])


class Car(models.Model):
    """Individual Car Listing"""
    TRANSMISSION_CHOICE = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('semi_Auto', 'Semi_Automatic'),
    ]

    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('plugin_hybrid', 'Plugin_Hybrid'),
    ]

    BODY_STYLE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'Suv'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('hatchback', 'Hatchback'),
        ('wagon', 'Wagon'),
        ('truck', 'Truck'),
    ]


    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name='cars')
    model = models.CharField(max_length=100)
    year = models.IntegerField(validators = [MinValueValidator(1900), MaxValueValidator(2024)])
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.IntegerField(help_text='Mileage in Kilometers/Miles')
    vin = models.CharField(max_length=17, unique=True, verbose_name="VIN")
    registration = models.CharField(max_length=20, blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_cars', blank=True)

    # Specifications
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICE)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    body_style = models.CharField(max_length=20, choices=BODY_STYLE_CHOICES)
    color = models.CharField(max_length=50)
    engine_size = models.CharField(max_length=50, help_text="e.g., 3.0L V6")
    horsepower = models.IntegerField(null=True, blank=True)
    doors = models.IntegerField(default=4)
    seats = models.IntegerField(default=5)

    # Descriptiuon
    description = models.TextField()
    features = models.TextField(help_text='List features separated by commas')

    # Status
    is_featured = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Images 
    main_image = models.ImageField(upload_to='cars/main/', blank=True)
    image_1 = models.ImageField(upload_to='cars/gallery/', blank=True)
    image_2 = models.ImageField(upload_to='cars/gallery/', blank=True)
    image_3 = models.ImageField(upload_to='cars/gallery/', blank=True)
    image_4 = models.ImageField(upload_to='cars/gallery/', blank=True)

    class Meta:
        ordering = ['-created_at', '-is_featured']
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['year']),
            models.Index(fields=['mileage']),
            models.Index(fields=['make', 'model']),
        ]

    def __str__(self):
        return f"{self.year} {self.make.name} {self.model}"

    def get_absolute_url(self):
        return reverse ('car_detail', args=[self.pk, self.slug])

    @property
    def slug(self):
        return slugify(f"{self.year}-{self.make.name}-{self.model}")

    @property
    def featured_image(self):
        """Get the correct image url"""
        if self.main_image and hasattr(self.main_image, 'url'):
            return self.main_image.url
        return "static/images/car-placeholder.jpg"

    def get_features_list(self):
        """Convert features string into list"""
        return [f.strip() for f in self.features.split(',') if f.strip()]
    
    @property
    def favorite_count(self):
        return self.favorited_by.count()
    
    def is_favorited_by(self, user):
        if user.is_autheticated:
            return self.favorited_by.filter(id=user.id).exists()
        return False
    
    @property
    def gallary_images(self):
        """Return list of all gallary images that exists"""
        images = []

        # Check each image field
        image_fields = ['image_1', 'image_2', 'image_3', 'image_4']
        for field_name in image_fields:
            image = getattr(self, field_name)
            if image and hasattr(image, 'url'):
                images.append(image.url)

        # If there are no gallary images but has only main images
        if not images and self.main_image and hasattr(self.main_image, 'url'):
            images.append(self.main_image.url)

        return images

    @property
    def all_images(self):
        """return all images including main"""
        images = []

        if self.main_image and hasattr(self.main_image, 'url'):
            images.append(self.main_image.url)

        images.extend(self.gallary_images)

        # Remove dublicates (If main image is also in the gallary)
        return list(dict.fromkeys(images))

    def save(self, *args, **kwargs):
        # Ensure that the main image has a default if not provided
        if not self.main_image:
            self.main_image = 'cars/main/default_car.jpg'
        super().save(*args, **kwargs)        


class Inquiry(models.Model):
    """Customer inquiry for cars"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    preferred_contact = models.CharField(max_length=10, choices=[('email', 'Email'), ('phone', 'Phone')], default='email')
    is_contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text='Internal notes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry for {self.car} by {self.name}"


class TestDrive(models.Model):
    """Test Drive Appointments"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='test_drives')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test drive for {self.car} by {self.name}"
            