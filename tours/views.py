from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .models import Monument, VirtualTour, Content
from .forms import ContentForm, SignupForm


class HomeView(ListView):
    model = Monument
    template_name = 'home.html'
    context_object_name = 'monuments'
    paginate_by = 15

    def get_queryset(self):
        return Monument.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contents'] = Content.objects.filter(status='published').order_by('-created_at')[:5]
        return context


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


# -------- CONTENT SYSTEM --------

@login_required
def create_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.created_by = request.user
            content.status = 'published'
            content.save()
            return redirect('tours:home')
    else:
        form = ContentForm()

    return render(request, 'tours/create_content.html', {'form': form})


@login_required
def edit_content(request, pk):
    content = get_object_or_404(Content, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return redirect('tours:profile')
    else:
        form = ContentForm(instance=content)

    return render(request, 'tours/edit_content.html', {'form': form})


@login_required
def delete_content(request, pk):
    content = get_object_or_404(Content, pk=pk, created_by=request.user)

    if request.method == 'POST':
        content.delete()
        return redirect('tours:profile')

    return render(request, 'tours/delete_content.html', {'content': content})


# -------- AUTH SYSTEM --------

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tours:home')
    else:
        form = SignupForm()

    return render(request, 'tours/signup.html', {'form': form})


@login_required
def profile(request):
    user_contents = Content.objects.filter(created_by=request.user).order_by('-created_at')

    return render(request, 'tours/profile.html', {
        'contents': user_contents
    })