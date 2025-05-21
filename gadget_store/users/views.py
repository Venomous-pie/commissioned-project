# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm
from .models import Profile
from cart.models import *
from django.contrib.auth.models import User


def auth_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    register_form = UserRegisterForm(prefix='register')
    login_form = UserLoginForm(prefix='login')

    if request.method == 'POST':
        if 'register-submit' in request.POST:
            register_form = UserRegisterForm(request.POST, prefix='register')
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.first_name = register_form.cleaned_data['first_name']
                user.last_name = register_form.cleaned_data['last_name']
                user.email = register_form.cleaned_data['email']
                user.save()
                Profile.objects.create(user=user)
                messages.success(request, f"Account created for {user.username}! You can now log in.")
                return redirect('auth')
            else:
                for field, errors in register_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                # Don't redirect, return the form with errors
                return render(request, 'users/auth.html', {
                    'register_form': register_form,
                    'login_form': login_form,
                    'active_tab': 'register'  # Add this to indicate the register tab should be active
                })

        elif 'login-submit' in request.POST:
            login_form = UserLoginForm(request.POST, prefix='login')
            if login_form.is_valid():
                identifier = login_form.cleaned_data.get('username_login')
                password = login_form.cleaned_data.get('password_login')

                # Attempt to get user by username or email
                try:
                    user_obj = User.objects.get(username=identifier)
                except User.DoesNotExist:
                    try:
                        user_obj = User.objects.get(email=identifier)
                    except User.DoesNotExist:
                        login_form.add_error('username_login', 'No account found with this username or email.')
                        return render(request, 'users/auth.html', {
                            'register_form': register_form,
                            'login_form': login_form,
                            'active_tab': 'login'  # Add this to indicate the login tab should be active
                        })

                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)
                    if user:
                        login(request, user)
                        messages.success(request, f"Welcome back, {user.username}!")

                        # Merge cart logic
                        if request.session.session_key:
                            session_cart = Cart.objects.filter(session_id=request.session.session_key).first()
                            if session_cart:
                                user_cart, _ = Cart.objects.get_or_create(user=user)
                                for item in session_cart.items.all():
                                    try:
                                        user_item = CartItem.objects.get(cart=user_cart, product=item.product)
                                        user_item.quantity += item.quantity
                                        user_item.save()
                                    except CartItem.DoesNotExist:
                                        item.cart = user_cart
                                        item.save()
                                session_cart.delete()

                        next_url = request.GET.get('next')
                        return redirect(next_url if next_url else '/')
                    else:
                        login_form.add_error('password_login', 'Incorrect password. Please try again.')
                        return render(request, 'users/auth.html', {
                            'register_form': register_form,
                            'login_form': login_form,
                            'active_tab': 'login'  # Add this to indicate the login tab should be active
                        })
                else:
                    login_form.add_error('username_login', 'No account found with this username or email.')
                    return render(request, 'users/auth.html', {
                        'register_form': register_form,
                        'login_form': login_form,
                        'active_tab': 'login'  # Add this to indicate the login tab should be active
                    })

            else:
                for field, errors in login_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                return render(request, 'users/auth.html', {
                    'register_form': register_form,
                    'login_form': login_form,
                    'active_tab': 'login'  # Add this to indicate the login tab should be active
                })

    return render(request, 'users/auth.html', {
        'register_form': register_form,
        'login_form': login_form
    })

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'users/profile.html', {'form': form})