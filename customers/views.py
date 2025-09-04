from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
import json

from .models import Customer, Address
from .forms import CustomerRegistrationForm, CustomerLoginForm, CustomerEditForm, AddressForm
from orders.models import Order


class LoginView(View):
    template_name = 'customers/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('customers:account')
        
        form = CustomerLoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomerLoginForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect to next URL or account page
            next_url = request.GET.get('next', 'customers:account')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_url)
        
        return render(request, self.template_name, {'form': form})


class RegisterView(View):
    template_name = 'customers/register.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('customers:account')
        
        form = CustomerRegistrationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to xCommerce, {user.first_name}!')
            return redirect('customers:account')
        
        return render(request, self.template_name, {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'customers/account.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Recent orders
        try:
            recent_orders = Order.objects.filter(customer=self.request.user).order_by('-created_at')[:5]
            context['recent_orders'] = recent_orders
            context['total_orders'] = Order.objects.filter(customer=self.request.user).count()
        except:
            context['recent_orders'] = []
            context['total_orders'] = 0
        
        # Addresses
        context['addresses'] = Address.objects.filter(customer=self.request.user, is_active=True)[:3]
        context['total_addresses'] = Address.objects.filter(customer=self.request.user, is_active=True).count()
        
        return context


class EditAccountView(LoginRequiredMixin, View):
    template_name = 'customers/edit_account.html'
    
    def get(self, request):
        form = CustomerEditForm(instance=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomerEditForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated successfully.')
            return redirect('customers:account')
        
        return render(request, self.template_name, {'form': form})


class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = 'customers/orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Order.objects.filter(customer=self.request.user).order_by('-created_at')
            
            # Search functionality
            search = self.request.GET.get('search')
            if search:
                queryset = queryset.filter(
                    Q(order_number__icontains=search) |
                    Q(status__icontains=search)
                )
            
            # Status filter
            status = self.request.GET.get('status')
            if status:
                queryset = queryset.filter(status=status)
            
            return queryset
        except:
            return Order.objects.none()


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'customers/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    
    def get_queryset(self):
        try:
            return Order.objects.filter(customer=self.request.user)
        except:
            return Order.objects.none()


# Address Management Views
class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'customers/addresses.html'
    context_object_name = 'addresses'
    
    def get_queryset(self):
        return Address.objects.filter(customer=self.request.user, is_active=True).order_by('-is_default', '-created_at')


class AddAddressView(LoginRequiredMixin, View):
    template_name = 'customers/add_address.html'
    
    def get(self, request):
        form = AddressForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AddressForm(request.POST)
        
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user
            
            # If this is the first address or marked as default, make it default
            if form.cleaned_data.get('is_default') or not Address.objects.filter(customer=request.user, is_active=True).exists():
                # Remove default from other addresses
                Address.objects.filter(customer=request.user, is_default=True).update(is_default=False)
                address.is_default = True
            
            address.save()
            messages.success(request, 'Address added successfully.')
            return redirect('customers:addresses')
        
        return render(request, self.template_name, {'form': form})


class EditAddressView(LoginRequiredMixin, View):
    template_name = 'customers/edit_address.html'
    
    def get(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, customer=request.user, is_active=True)
        form = AddressForm(instance=address)
        return render(request, self.template_name, {'form': form, 'address': address})
    
    def post(self, request, address_id):
        address = get_object_or_404(Address, id=address_id, customer=request.user, is_active=True)
        form = AddressForm(request.POST, instance=address)
        
        if form.is_valid():
            updated_address = form.save(commit=False)
            
            # Handle default address logic
            if form.cleaned_data.get('is_default'):
                Address.objects.filter(customer=request.user, is_default=True).update(is_default=False)
                updated_address.is_default = True
            
            updated_address.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('customers:addresses')
        
        return render(request, self.template_name, {'form': form, 'address': address})


@login_required
def delete_address(request, address_id):
    if request.method == 'POST':
        address = get_object_or_404(Address, id=address_id, customer=request.user, is_active=True)
        
        # Don't allow deletion of the last address if it's default
        remaining_addresses = Address.objects.filter(customer=request.user, is_active=True).exclude(id=address_id)
        
        if address.is_default and remaining_addresses.exists():
            # Make another address default
            remaining_addresses.first().update(is_default=True)
        
        address.is_active = False
        address.save()
        
        messages.success(request, 'Address deleted successfully.')
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True})
    
    return redirect('customers:addresses')
