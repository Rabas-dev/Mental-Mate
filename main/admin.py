from django.contrib import admin
from .models import Chatbot, BlogPost, WellnessEntry

@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'get_primary_focus_display', 'created_at')
    list_filter = ('primary_focus', 'created_at')
    search_fields = ('name', 'user__username', 'specific_concerns')
    date_hierarchy = 'created_at'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_category_display', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'

@admin.register(WellnessEntry)
class WellnessEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mood', 'sleep_hours', 'energy_level', 'anxiety_level')
    list_filter = ('date', 'mood')
    search_fields = ('user__username', 'notes')
    date_hierarchy = 'date'
