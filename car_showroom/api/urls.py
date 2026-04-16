from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



schema_view = get_schema_view(
    openapi.Info(
        title="CAR Showroom API",
        default_version='v1',
        description="API documemtation for luxury Car Showroom",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@luxurycars.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'makes', views.MakeViewSet)
router.register(r'cars', views.CarViewSet)
router.register(r'inquires', views.InquiryViewSet, basename='inquiry')
router.register(r'test-drive', views.TestDriveViewSet, basename='testdrive')
router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', obtain_auth_token, name='api_token_auth'),
    path('auth/register/', views.UserViewSet.as_view({'post': 'register'}), name='api_register'),
    path('auth.profile/', views.UserViewSet.as_view({'get': 'profile'}), name='api_profile'),
    path('auth/profile/update/', views.UserViewSet.as_view({'put': 'update_profile'}), name='api_update_profile'),
    path('auth/favorites/add/', views.UserViewSet.as_view({'post': 'add_favorite'}), name='api_add_favorite'),
    path('auth/favporite/remove/', views.UserViewSet.as_view({'post': 'remove_favorite'}), name='api_remove_favorite'),
    path('search/', views.SearchView.as_view(), name='api_search'),
    path('statistics/', views.StatisticsView.as_view(), name='api_statistics'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]