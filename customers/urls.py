from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # Authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Account Management
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/edit/', views.EditAccountView.as_view(), name='edit_account'),
    path('orders/', views.OrderHistoryView.as_view(), name='orders'),
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    # Address Management
    path('addresses/', views.AddressListView.as_view(), name='addresses'),
    path('addresses/add/', views.AddAddressView.as_view(), name='add_address'),
    path('addresses/<int:address_id>/edit/', views.EditAddressView.as_view(), name='edit_address'),
    path('addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
]