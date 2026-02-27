from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import models
from .models import Monument, VirtualTour
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


class HomeView(ListView):
    model = Monument
    template_name = 'home.html'
    context_object_name = 'monuments'
    paginate_by = 15

    def get_queryset(self):
        return Monument.objects.all().order_by('-created_at')


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


def search(request):
    query = request.GET.get('q', '')
    monuments = []

    if query:
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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')  # 👈 CHANGED FROM 'login' TO '/login/'
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')