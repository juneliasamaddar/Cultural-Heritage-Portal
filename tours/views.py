from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import models
from .models import Monument, VirtualTour


class HomeView(ListView):
    model = Monument
    template_name = 'home.html'
    context_object_name = 'monuments'

    def get_queryset(self):
        # Get all monuments, but prioritize those with images
        return Monument.objects.all().order_by('-main_image', 'name')[:6]

class MonumentDetailView(DetailView):
    model = Monument
    template_name = 'tours/monument_detail.html'
    context_object_name = 'monument'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tours'] = VirtualTour.objects.filter(
            monument=self.object,
            is_published=True
        )
        return context


class VirtualTourView(DetailView):
    model = VirtualTour
    template_name = 'tours/virtual_tour.html'
    context_object_name = 'tour'


# Search function
def search(request):
    query = request.GET.get('q', '')
    monuments = []

    if query:
        # Search in name, location, state, and description
        monuments = Monument.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(location__icontains=query) |
            models.Q(state__icontains=query) |
            models.Q(description__icontains=query)
        ).distinct()

    context = {
        'monuments': monuments,
        'query': query,
        'count': monuments.count() if monuments else 0
    }
    return render(request, 'search_results.html', context)
