from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Chatbot(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Non-binary'),
    ]
    
    FOCUS_CHOICES = [
        ('ANX', 'Anxiety'),
        ('DEP', 'Depression'),
        ('STR', 'Stress'),
        ('REL', 'Relationships'),
        ('SLE', 'Sleep'),
        ('MIN', 'Mindfulness'),
        ('GEN', 'General Support'),
        ('PATCHUP', 'Patchup'),
    ]
    
    PERSONALITY_CHOICES = [
        ('empathetic', 'Empathetic Listener'),
        ('motivational', 'Motivational Coach'),
        ('calm', 'Calm Supporter'),
        ('cheerful', 'Cheerful Friend'),
        ('practical', 'Practical Advisor'),
        ('just_like_her', 'Just Like Her'),
        ('just_like_him', 'Just Like Him'),
    ]
    
    AVATAR_CHOICES = [
        ('/static/main/avatars/avatar1.png', 'Blue Bot'),
        ('/static/main/avatars/avatar2.png', 'Green Bot'),
        ('/static/main/avatars/avatar3.png', 'Purple Bot'),
        ('/static/main/avatars/avatar4.png', 'Orange Bot'),
        ('/static/main/avatars/avatar5.png', 'Pink Bot'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    primary_focus = models.CharField(max_length=8, choices=FOCUS_CHOICES)
    specific_concerns = models.TextField()
    additional_context = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.png')
    personality = models.CharField(max_length=20, choices=PERSONALITY_CHOICES, default='empathetic')
    
    def __str__(self):
        return f"{self.name} - {self.get_primary_focus_display()}"

class ChatMessage(models.Model):
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender} ({self.timestamp:%Y-%m-%d %H:%M}): {self.message[:30]}"

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('ANX', 'Anxiety'),
        ('DEP', 'Depression'),
        ('MIN', 'Mindfulness'),
        ('STR', 'Work Stress'),
        ('REL', 'Relationships'),
        ('CAR', 'Self-Care'),
        ('SLE', 'Sleep'),
        ('THR', 'Therapy'),
        ('EXE', 'Exercise'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class WellnessEntry(models.Model):
    MOOD_CHOICES = [
        (1, '😭 Very Sad'),
        (2, '😔 Sad'),
        (3, '😐 Neutral'),
        (4, '🙂 Good'),
        (5, '😃 Very Good'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    mood = models.IntegerField(choices=MOOD_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    sleep_hours = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(24)], null=True, blank=True)
    energy_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    anxiety_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s wellness entry for {self.date}"

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create premade chatbots for demo purposes.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user, _ = User.objects.get_or_create(username='demo', defaults={'password': 'demo'})
        from main.models import Chatbot
        premade_bots = [
            {
                'name': 'Sunny',
                'gender': 'F',
                'primary_focus': 'MIN',
                'specific_concerns': 'Helping you find daily joy and mindfulness.',
                'additional_context': 'Loves meditation and positive affirmations.',
                'avatar': '/static/main/avatars/avatar1.png',
                'personality': 'cheerful',
            },
            {
                'name': 'Coach Max',
                'gender': 'M',
                'primary_focus': 'STR',
                'specific_concerns': 'Motivating you to overcome stress and reach your goals.',
                'additional_context': 'Enjoys sports and self-improvement books.',
                'avatar': '/static/main/avatars/avatar2.png',
                'personality': 'motivational',
            },
            {
                'name': 'Dr. Calm',
                'gender': 'N',
                'primary_focus': 'ANX',
                'specific_concerns': 'Guiding you through anxiety with empathy and calm.',
                'additional_context': 'Expert in breathing exercises and relaxation.',
                'avatar': '/static/main/avatars/avatar3.png',
                'personality': 'calm',
            },
        ]
        for bot in premade_bots:
            Chatbot.objects.get_or_create(user=user, name=bot['name'], defaults=bot)
        self.stdout.write(self.style.SUCCESS('Premade chatbots created.'))
