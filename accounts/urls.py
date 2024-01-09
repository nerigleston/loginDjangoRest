from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('test_token', views.test_token),
    path('get_all_users', views.getAllUsers),
    path('delete_user/<int:id>', views.deleteUser),
]
