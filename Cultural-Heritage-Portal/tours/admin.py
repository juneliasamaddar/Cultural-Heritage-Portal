from django.contrib import admin
from .models import Monument, MonumentImage, VirtualTour

class MonumentImageInline(admin.TabularInline):
    model = MonumentImage
    extra = 3  # Show 3 empty image fields

class VirtualTourInline(admin.TabularInline):
    model = VirtualTour
    extra = 1

@admin.register(Monument)
class MonumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'state', 'period', 'dynasty', 'created_at']
    list_filter = ['state', 'dynasty', 'period']
    search_fields = ['name', 'location', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MonumentImageInline, VirtualTourInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short_description', 'description')
        }),
        ('Location Details', {
            'fields': ('location', 'state', ('latitude', 'longitude'))
        }),
        ('Historical Info', {
            'fields': ('period', 'dynasty')
        }),
        ('Visitor Info', {
            'fields': ('visiting_hours', 'entry_fee')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
    )

@admin.register(MonumentImage)
class MonumentImageAdmin(admin.ModelAdmin):
    list_display = ['monument', 'caption', 'is_primary']
    list_filter = ['monument', 'is_primary']

@admin.register(VirtualTour)
class VirtualTourAdmin(admin.ModelAdmin):
    list_display = ['title', 'monument', 'tour_type', 'duration_minutes', 'is_published']
    list_filter = ['tour_type', 'is_published', 'monument']
    search_fields = ['title', 'description']