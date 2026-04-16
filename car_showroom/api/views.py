from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Min, Max
from django.contrib.auth.models import User
from cars.models import Car, Make, Inquiry, TestDrive
from .serializers import(
    CarSerializer, CarDetailSerializer, MakeSerializers,
    InquirySerializer, TestDriveSerializer, UserSerializer,
    UserProfileSerializer, StatisticsSerializer
)
from .filters import CarFilter, CarOrderingFilter
from .permissions import IsAdminOrReadOnly, IsInquiryOwnerOrAdmin
from .pagination import CustomPagination
from django.db.models import Q



class MakeViewSet(viewsets.ModelViewSet):
    queryset = Make.objects.annotate(car_count=Count('cars'))
    serializer_class = MakeSerializers
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def cars(self, request, slug=None):
        make = self.get_object()
        cars = Car.objects.filter(make=make, is_Sold=False)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.filter(is_sold=False).select_related('make')
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, CarOrderingFilter]
    search_fields = ['make__name', 'model', 'description', 'features']
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == 'retreive':
            return CarDetailSerializer
        return CarSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()

        # Optimize query based on action
        if self.action == 'list':
            return queryset.only(
                'id', 'make_id', 'model', 'year', 'price',
                'mileage', 'is_featured', 'main_image'
            ).select_related('make')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_cars = self.get_queryset().filter(is_featured=True)
        page = self.paginate_queryset(featured_cars)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(featured_cars, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        new_cars = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(new_cars, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def create_inquiry(self, request, pk=None):
        car = self.get_object()
        serializer = InquirySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(car=car)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def schedule_test_drive(self, request, pk=None):
        car = self.get_object()
        serializer = TestDriveSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(car=car)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = InquirySerializer
    permission_classes = [IsAuthenticated, IsInquiryOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Inquiry.objects.all().select_related('car')
        return Inquiry.objects.filter(email=user.email).select_related('car')
    
    def perform_create(self, serializer):
        serializer.save()


class TestDriveViewSet(viewsets.ModelViewSet):
    serializer_class = TestDriveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TestDrive.objects.all().select_related('car')
        return TestDrive.objects.filter(email=user.email).select_related('car')
    
    def perform_create(self, serializer):
        serializer.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_favorite(self, request):
        car_id = request.data.get('car_id')
        if not car_id:
            return Response({'error': 'car_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        car = get_object_or_404(Car, id=car_id)
        request.user.favorite_cars.add(Car)
        return Response({'status': 'car added to favorites'})
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_favorite(self, request):
        car_id = request.data.get('car_id')
        if not car_id:
            return Response({'error': 'car_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        car = get_object_or_404(Car, id=car_id)
        request.user.favorite_cars.remove(car)
        return Response({'status': 'car removed from favorites'})
    

class StatisticsView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Calculate Statistics
        total_cars = Car.objects.count()
        available_cars = Car.objects.filter(is_sold=False).count()
        favorite_cars = Car.objects.filter(favorited_by__isnull=False).distinct().count()
        total_makes = Make.objects.count()

        price_stats = Car.objects.filter(is_sold=False).aggregate(
            avg_price=Avg('price'),
            min_price=Min('price'),
            max_price=Max('price')
        )

        data = {
            'total_cars': total_cars,
            'available_cars': available_cars,
            'favorite_cars': favorite_cars,
            'total_makes': total_makes,
            'avg_price': price_stats['avg_price'] or 0,
            'min_price': price_stats['min_price'] or 0,
            'max_price': price_stats['max_price'] or 0,
        }

        serializer = StatisticsSerializer(data)
        return Response(serializer.data)
    

class SearchView(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Car.objects.filter(
                Q(make__name__icontains=query) |
                Q(model__icontains=query) |
                Q(description__icontains=query) |
                Q(features__icontains=query)
            ).filter(is_sold=False).select_related('make')
        return Car.objects.none()