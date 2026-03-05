from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('dashboard/customer/', views.CustomerDashboardAPIView.as_view(), name='customer_dashboard'),
    path('dashboard/admin/', views.AdminDashboardAPIView.as_view(), name='admin_dashboard'),
    path('api/admin/users/<int:user_id>/', views.AdminDeleteUserAPIView.as_view(), name='delete_user'),
    path('api/admin/users/<int:user_id>/edit/', views.AdminEditUserAPIView.as_view(), name='edit_user'),
]