from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'tours'

urlpatterns = [
    # Home and Monument URLs
    path('', views.HomeView.as_view(), name='home'),
    path('monument/<slug:slug>/', views.MonumentDetailView.as_view(), name='monument_detail'),
    path('tour/<int:pk>/', views.VirtualTourView.as_view(), name='virtual_tour'),
    path('search/', views.search, name='search'),

    # AUTHENTICATION URLs - ALL 4 MUST BE HERE
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),  # 👈 THIS MUST BE HERE
    path('profile/', views.profile, name='profile'),
]