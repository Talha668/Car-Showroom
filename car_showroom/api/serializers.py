from rest_framework import serializers
from cars.models import Car, Make, Inquiry, TestDrive
from django.contrib.auth.models import User
from django.utils.timezone import now




class MakeSerializers(serializers.ModelSerializer):
    car_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Make
        fields = ['id', 'name', 'country', 'founded_year', 'logo', 'slug', 'car_count', 'website']
        read_only_fields = ['slug']


class CarSerializer(serializers.ModelSerializer):
    make = MakeSerializers(read_only=True)
    make_id = serializers.PrimaryKeyRelatedField(
        queryset=Make.objects.all(),
        source='make',
        write_only=True
    )
    features_list = serializers.ListField(
        child=serializers.CharField(),
        source='get_geatured_list',
        read_only=True
    )
    is_available = serializers.BooleanField(
        source='is_sold',
        read_only=True
    )

    class Meta:
        model = Car
        fields = [
            'id', 'make', 'make_id', 'model', 'year', 'price', 'mileage',
            'vin', 'registration', 'transmission', 'fuel_type', 'body_style',
            'color', 'engine_size', 'horsepower', 'doors', 'seats',
            'description', 'features', 'features_list', 'is_featured',
            'is_sold', 'is_reserved', 'is_available', 'main_image',
            'image_1', 'image_2', 'image_3', 'image_4', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_year(Self, value):
        current_year = now().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(f"Year must be between 1900 and {current_year + 1}")
        return value
    

class CarDetailSerializer(CarSerializer):
    # extend serializer for detail view
    similar_cars = serializers.SerializerMethodField()

    class Meta(CarSerializer.Meta):
        fields = CarSerializer.Meta.fields + ['similar_cars']

    def similar_cars(self, obj):
        similar = Car.objects.filter(
            make = obj.make,
            is_sold = False
        ).exclude(id=obj.id)[:4]
        return CarSerializer(similar, many=True, context=self.context).data


class InquirySerializer(serializers.ModelSerializer):
    car_details = CarSerializer(source='car', read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        queryset = Car.objects.filter(is_sold=False),
        write_only=True
    )
    user_email = serializers.EmailField(source='email', required=True)

    class Meta:
        model = Inquiry
        fields = [
            'id', 'car', 'car_details', 'car_id', 'name', 'user_email',
            'phone', 'message', 'preferred_contact', 'is_contacted',
            'notes', 'created_at'
        ]
        read_only_fields = ['is_contacted', 'notes', 'created_at']

        def created(self, validated_data):
            # Auto set car from car_id
            validated_data['car'] = validated_data.pop['car_id']
            return super().create(validated_data)
        

class TestDriveSerializer(serializers.ModelSerializer):
    car_detail = CarSerializer(source='car', read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.filter(is_sold=False),
        write_only=True
    )

    class Meta:
        model = TestDrive
        fileds = [
            'id', 'car', 'car_details', 'car_id', 'name', 'email',
            'phone', 'preferred_date', 'preferred_time', 'message',
            'is_confirmed', 'created_at'
        ]
        read_only_fields = ['is_confirmed', 'created_at']

        def validated_preferred_date(self, value):
            if value < now().date():
                raise serializers.ValidationError("Test drive cannot be in the past")
            return value
        

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data('email', ''),
            password=validated_data['password'],
            first_name=validated_data('first_name', ''),
            last_name=validated_data('last_name', '')
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    favorite_cars = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Car.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'favorite_cars']
        read_only_fields = ['username']


class StatisticsSerializer(serializers.Serializer):
    total_cars = serializers.IntegerField()
    available_cars = serializers.IntegerField()
    favorite_cars = serializers.IntegerField()
    total_makes = serializers.IntegerField()
    avg_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
