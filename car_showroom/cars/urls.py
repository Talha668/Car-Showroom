from django.urls import path
from . import views


urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('search/', views.car_search, name='car_search'),
    path('<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('<int:pk>/<slug:slug>/', views.CarDetailView.as_view(), name='car_detail_slug'),
    path('make/<slug:make_slug>/', views.CarsByMakeView.as_view(), name='cars_by_make'),
    path('featured/', views.FeaturedCarsView.as_view(), name='featured_cars'),
    path('new-arrivals/', views.NewArrivalsView.as_view(), name='new_arrivals'),
    path('inquiry/<int:car_id>/', views.create_inquiry, name='create_inquiry'),
    path('test-drive/<int:car_id>/', views.schedule_test_drive, name='schedule_test_drive'),
]