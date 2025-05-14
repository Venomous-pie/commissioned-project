# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm
from .models import Profile

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    register_form = UserRegisterForm(prefix='register')
    login_form = UserLoginForm(prefix='login')

    if request.method == 'POST':
        if 'register-submit' in request.POST:
            register_form = UserRegisterForm(request.POST, prefix='register')
            if register_form.is_valid():
                user = register_form.save()
                Profile.objects.create(user=user)
                messages.success(request, f"Account created for {user.username}! You can now log in.")
                return redirect('auth')  # Stay on same page for login
        elif 'login-submit' in request.POST:
            login_form = UserLoginForm(request.POST, prefix='login')
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome back, {username}!")

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
                    messages.error(request, 'Invalid username or password.')

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