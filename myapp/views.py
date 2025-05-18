from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Contact, Service
from .models import AboutUs
from .models import CustomUser
from .models import Users, Category  # Added Users and Category
from .models import Review  # Add this import
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import UserProfile
from .forms import UserProfileForm

def home(request):
    reviews = Review.objects.filter(is_active=True)
    return render(request, 'index.html', {'reviews': reviews})

def about(request):
    # Get users with their related category information
    users = Users.objects.select_related('category').all()
    about_sections = AboutUs.objects.all()
    return render(request, 'about.html', {
        'about': about_sections,
        'users': users
    })

def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'service_detail.html', {'service': service})

def contact(request):
    return render(request, 'contact.html')

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Create new contact entry
        contact = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('/#contact')  # Redirect back to contact section
    
    return redirect('/')  # Redirect to home if not POST

def submit_review(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        photo = request.FILES.get('photo')
        
        review = Review.objects.create(
            name=name,
            rating=rating,
            comment=comment,
            photo=photo,
            is_active=True
        )
        
        messages.success(request, 'Thank you for your review!')
        return redirect('/#reviews')
    
    return redirect('/')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def about_us(request):
    # Fetch users with related data using select_related()
    users = Users.objects.select_related('category').all()
    
    return render(request, 'myapp/about_us.html', {
        'users': users
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Update last login IP
                if hasattr(user, 'profile'):
                    user.profile.last_login_ip = request.META.get('REMOTE_ADDR')
                    user.profile.save()
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile for the new user
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone', ''),
                address=form.cleaned_data.get('address', '')
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})
    user_profile = request.user.profile
    return render(request, 'myapp/profile.html', {'profile': user_profile})
