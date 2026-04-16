from django.contrib import admin
from django.utils.html import format_html
from . models import Car, Make, TestDrive, Inquiry



@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year', 'car_count')
    search_fields = ('name', 'country')
    prepopulated_fields = {'slug': ('name',)}

    def car_count(self, obj):
        return obj.cars.count()
    car_count.short_description = 'Number of cars'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make_model_year', 'price', 'mileage', 'is_featured', 'created_at', 'is_sold', 'image_preview')
    list_filter = ('make', 'year', 'fuel_type', 'transmission', 'is_featured', 'is_sold')
    search_fields = ('make__name', 'model', 'vin', 'description')
    list_editable = ('price', 'is_sold', 'is_featured')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('make', 'model', 'year', 'price', 'mileage', 'vin', 'registration')
        }),
        ('Specifications', {
            'fields': ('transmission', 'fuel_type', 'body_style', 'color', 'engine_size', 'horsepower', 'doors', 'seats')
        }),
        ('Descriptions and Features', {
            'fields': ('description', 'features')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_sold', 'is_reserved')
        }),
        ('Images', {
            'fields':('main_image', 'image_1', 'image_2', 'image_3', 'image_4'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }), 
    )

    def make_model_year(self, obj):
        return f"{obj.year} {obj.make.name} {obj.model}"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('make')
    
    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height: 50px;" />', obj.main_image.url)
        return "No image"
    image_preview.short_description = 'Preview'
    

@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = ('car', 'name', 'preferred_date', 'preferred_time', 'is_confirmed')
    list_filter = ('is_confirmed', 'preferred_date')
    search_fields = ('name', 'email', 'car__make__name')
    list_editable = ('is_confirmed',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('car', 'name', 'email', 'is_contacted', 'created_at')
    list_filter = ('is_contacted', 'preferred_contact', 'created_at')
    search_fields = ('name', 'email', 'car__make__name', 'car__model')
    readonly_fields = ('created_at',)
    list_editable = ('is_contacted',)