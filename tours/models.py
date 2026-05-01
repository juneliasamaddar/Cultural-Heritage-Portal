from django.db import models
from django.contrib.auth.models import User


class Monument(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    location = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    period = models.CharField(max_length=100)
    dynasty = models.CharField(max_length=100)
    visiting_hours = models.CharField(max_length=200, default="10:00 AM - 6:00 PM")
    entry_fee = models.CharField(max_length=200, blank=True, default="Free")

    # Images
    main_image = models.ImageField(upload_to='monuments/main/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MonumentImage(models.Model):
    monument = models.ForeignKey(Monument, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='monuments/gallery/', null=True, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.monument.name}"


class VirtualTour(models.Model):
    TOUR_TYPES = [
        ('360', '360° Interactive Tour'),
        ('video', 'Video Tour'),
        ('audio', 'Audio Guide'),
    ]

    title = models.CharField(max_length=200)
    monument = models.ForeignKey(Monument, on_delete=models.CASCADE, related_name='tours')
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES)

    # For 360° tours
    panorama_image = models.ImageField(upload_to='tours/360/', null=True, blank=True)

    # For video tours
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='tours/videos/', null=True, blank=True)

    # For audio guides
    audio_file = models.FileField(upload_to='tours/audio/', null=True, blank=True)

    description = models.TextField()
    duration_minutes = models.IntegerField(default=30)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.monument.name}"

class Content(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)

    image = models.ImageField(upload_to='content/', null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contents')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CreatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username