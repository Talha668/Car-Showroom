from django_filters import rest_framework as filters
from cars.models import Car
from django.db.models import Q



class CarFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_year = filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = filters.NumberFilter(field_name='year', lookup_expr='lte')
    min_mileage = filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    max_mileage = filters.NumberFilter(field_name='mileage', lookup_expr='lte')
    make = filters.CharFilter(field_name='make__name', lookup_expr='iexact')
    make_slug = filters.CharFilter(field_name='make__slug', lookup_expr='exact')
    transmission = filters.CharFilter(field_name='transmission', lookup_expr='iexact')
    fuel_type = filters.CharFilter(field_name='fuel_type', lookup_expr='iexact')
    body_style = filters.CharFilter(field_name='body_style', lookup_expr='iexact')
    featured = filters.BooleanFilter(field_name='is_featured')
    available = filters.BooleanFilter(method='filter_available')
    
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = Car
        fields = [
            'min_price', 'max_price', 'min_year', 'max_year',
            'min_mileage', 'max_mileage', 'make', 'make_slug',
            'transmission', 'fuel_type', 'body_style', 'featured',
            'available', 'search'
        ]

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(is_sold=False)
        return queryset.filter(is_sold=True)

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(make__name__icontains=value) |
            Q(model__icontains=value) |
            Q(description__icontains=value) |
            Q(features__icontains=value)
        )


class CarOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            # Map API-friendle field name to model field name
            field_mapping = {
                'price': 'price',
                'year': 'year',
                'mileage': 'mileage',
                'created_at': 'created_at',
                'make': 'make__name',
            }

            mapped_ordering = []
            for field in ordering:
                if field.startswith('-'):
                    db_field = field_mapping.get(field[1:])
                    if db_field:
                        mapped_ordering.append(f'-{db_field}')
                else:
                    db_field = field_mapping.get(field)
                    if db_field:
                        mapped_ordering.append(db_field)

            return queryset.order_by(*mapped_ordering)

        return queryset                    