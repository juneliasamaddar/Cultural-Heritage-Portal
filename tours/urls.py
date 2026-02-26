from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('monument/<slug:slug>/', views.MonumentDetailView.as_view(), name='monument_detail'),
    path('tour/<int:pk>/', views.VirtualTourView.as_view(), name='virtual_tour'),
    path('search/', views.search, name='search'),  # Search functionality
]