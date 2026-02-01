from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('farm:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome to Poultry-Pro, {user.get_full_name()}!')
            
            # Redirect based on role
            if user.is_farmer:
                return redirect('farm:dashboard')
            elif user.is_seller:
                return redirect('orders:marketplace')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})




def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('farm:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                
                # Redirect to next parameter or dashboard
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                # Redirect based on role
                if user.is_farmer:
                    return redirect('farm:dashboard')
                elif user.is_seller:
                    return redirect('orders:marketplace')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_redirect(request):
    """Redirect users to appropriate dashboard based on role"""
    if request.user.is_farmer:
        return redirect('farm:dashboard')
    elif request.user.is_seller:
        return redirect('orders:marketplace')
    else:
        return redirect('home')