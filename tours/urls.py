from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'tours'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('monument/<slug:slug>/', views.MonumentDetailView.as_view(), name='monument_detail'),
    path('tour/<int:pk>/', views.VirtualTourView.as_view(), name='virtual_tour'),
    path('search/', views.search, name='search'),  # Search functionality
    path('create-content/', views.create_content, name='create_content'),
    path('login/', auth_views.LoginView.as_view(template_name='tours/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='tours:home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('edit-content/<int:pk>/', views.edit_content, name='edit_content'),
    path('delete-content/<int:pk>/', views.delete_content, name='delete_content'),
]