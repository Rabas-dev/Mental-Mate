from django import forms
from .models import Chatbot, BlogPost, WellnessEntry

class ChatbotForm(forms.ModelForm):
    class Meta:
        model = Chatbot
        fields = ['name', 'gender', 'primary_focus', 'specific_concerns', 'additional_context', 'avatar', 'personality']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'primary_focus': forms.Select(attrs={'class': 'form-control'}),
            'specific_concerns': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'additional_context': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'personality': forms.Select(attrs={'class': 'form-control'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class WellnessEntryForm(forms.ModelForm):
    class Meta:
        model = WellnessEntry
        fields = ['mood', 'sleep_hours', 'energy_level', 'anxiety_level', 'notes']
        widgets = {
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'energy_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'anxiety_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }