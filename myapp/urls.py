from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('about-us/', views.about_us, name='about_us'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('appointments/', views.appointments_view, name='appointments'),
    path('appointments/<int:pk>/delete/', views.delete_appointment, name='delete_appointment'),
    path('appointments/<int:pk>/edit/', views.edit_appointment, name='edit_appointment'),
    # Add this to the existing urlpatterns list
    path('chat/', views.ai_chat_view, name='ai_chat'),
]
