from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from cars.models import Car, Make
from api.serializers import CarSerializer, MakeSerializers



@api_view(['get'])
@permission_classes([AllowAny])
def homepage_data(request):
    """API request for homepage data"""
    featured_cars = Car.objects.filter(is_featured=True, is_sold=False)[:6]
    new_arrival = Car.objects.filter(is_sold=False).order_by('-created_at')[:6]
    makes = Make.objects.all()[:10]

    return Response({
        'featured_cars': CarSerializer(featured_cars, many=True).data,
        'new_Arrival': CarSerializer(new_arrival, many=True).data,
        'make': MakeSerializers(makes, many=True).data,
    })