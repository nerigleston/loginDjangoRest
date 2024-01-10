from django.urls import path, include
from . import views
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Login",
        default_version='v1',
        description="API Teste Login - Django Rest Framework",
        # terms_of_service="https://www.suaapi.com/terms/",
        # contact=openapi.Contact(email="contato@suaapi.com"),
        # license=openapi.License(name="Sua Licença"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('test_token', views.test_token),
    path('get_all_users', views.getAllUsers),
    path('delete_user/<int:id>', views.deleteUser),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]
