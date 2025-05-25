from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json
import requests
from .models import Chatbot, BlogPost, WellnessEntry
from .forms import ChatbotForm, BlogPostForm, WellnessEntryForm
from voice_call.eleven_labs import text_to_speech

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, 'Account created successfully! Welcome to MentalMate.')
            return redirect('dashboard')
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

@login_required
def logout_view(request):
    messages.info(request, 'You have been successfully logged out.')
    auth.logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    chatbots = Chatbot.objects.filter(user=request.user)
    blog_posts = BlogPost.objects.all().order_by('-created_at')[:5]
    
    # Get last 7 days of wellness data
    last_week = timezone.now().date() - timedelta(days=7)
    wellness_entries = WellnessEntry.objects.filter(
        user=request.user,
        date__gte=last_week
    ).order_by('date')

    # Calculate wellness score (average of mood, energy, and inverse anxiety)
    latest_entry = wellness_entries.last()
    wellness_score = 0
    if latest_entry:
        mood_score = (latest_entry.mood / 5) * 100
        energy_score = (latest_entry.energy_level / 10) * 100 if latest_entry.energy_level else 0
        anxiety_score = (10 - latest_entry.anxiety_level if latest_entry.anxiety_level else 5) * 10
        wellness_score = int((mood_score + energy_score + anxiety_score) / 3)

    return render(request, 'main/dashboard.html', {
        'chatbots': chatbots,
        'blog_posts': blog_posts,
        'wellness_entries': wellness_entries,
        'wellness_score': wellness_score
    })

class ChatbotListView(LoginRequiredMixin, ListView):
    model = Chatbot
    template_name = 'main/chatbot_list.html'
    context_object_name = 'chatbots'

    def get_queryset(self):
        return Chatbot.objects.filter(user=self.request.user)

class ChatbotCreateView(LoginRequiredMixin, CreateView):
    model = Chatbot
    form_class = ChatbotForm
    template_name = 'main/chatbot_form.html'
    success_url = reverse_lazy('chatbot-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ChatbotUpdateView(LoginRequiredMixin, UpdateView):
    model = Chatbot
    form_class = ChatbotForm
    template_name = 'main/chatbot_form.html'
    success_url = reverse_lazy('chatbot-list')

    def get_queryset(self):
        return Chatbot.objects.filter(user=self.request.user)

class ChatbotDeleteView(LoginRequiredMixin, DeleteView):
    model = Chatbot
    template_name = 'main/chatbot_confirm_delete.html'
    success_url = reverse_lazy('chatbot-list')

    def get_queryset(self):
        return Chatbot.objects.filter(user=self.request.user)

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'main/blog_list.html'
    context_object_name = 'blog_posts'
    ordering = ['-created_at']
    paginate_by = 10

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'main/blog_detail.html'
    context_object_name = 'post'

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'main/blog_form.html'
    success_url = reverse_lazy('blog-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'main/blog_form.html'
    success_url = reverse_lazy('blog-list')

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'main/blog_confirm_delete.html'
    success_url = reverse_lazy('blog-list')

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

@csrf_exempt
@login_required
def character_chat(request):
    chatbot_id = request.POST.get('chatbot_id') or request.GET.get('chatbot_id')
    if request.method == 'POST' and chatbot_id:
        user_message = request.POST.get('message')
        chatbot = Chatbot.objects.get(id=chatbot_id, user=request.user)
        # Premade prompt template
        if chatbot.get_primary_focus_display().lower() == 'patchup' and chatbot.personality in ['just_like_her', 'just_like_him']:
            prompt = (
                "You are the user's ex-" + ("girlfriend" if chatbot.personality == 'just_like_her' else "boyfriend") + ". "
                "You left the user some time ago. Now you are talking to them as their ex, with all the emotional complexity, nostalgia, and realism of such a conversation. "
                "Be authentic, sometimes caring, sometimes distant, sometimes regretful, sometimes playful, just like a real ex would be. "
                "Do not be robotic. Use natural, human, and emotionally nuanced language.And make human like short and concise responses just like a real ex would on whatsapp chat. "
                "Stay in character as the ex at all times.\n"
                f"User: {user_message}\nEx:" 
            )
        # Default prompt for all other categories and personalities
        else:
            prompt_template = (
                "You are {name}, a {personality} AI companion. "
                "Your main focus is: {focus}. "
                "Respond to the user in a short, concise, and human-like manner, similar to WhatsApp chats. "
                "Use natural language and include related emojis to make the conversation engaging. "
                "Stay in character and be supportive, friendly, and helpful.\n"
                "User: {user_message}\n{name}:"
            )
            prompt = prompt_template.format(
                name=chatbot.name,
                personality=chatbot.get_personality_display(),
                focus=chatbot.get_primary_focus_display(),
                user_message=user_message
            )
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 200,
        }
        response = requests.post(api_url, headers=headers, json=data)
        try:
            resp_json = response.json()
            if 'error' in resp_json:
                error_str = str(resp_json['error'])
                if 'quota' in error_str.lower() or 'limit' in error_str.lower():
                    reply = "Sorry, the AI service is currently unavailable due to usage limits. Please try again later."
                else:
                    reply = f"AI Error: {error_str}"
            else:
                reply = resp_json['choices'][0]['message']['content']
        except Exception as e:
            reply = f"Sorry, I couldn't get a response from the AI. (Error: {str(e)})"
        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "Invalid request."}, status=400)

@login_required
def chatbot_list_json(request):
    chatbots = Chatbot.objects.filter(user=request.user)
    data = {
        "chatbots": [
            {
                "id": bot.id,
                "name": bot.name,
                "avatar": bot.avatar.url if hasattr(bot.avatar, 'url') else bot.avatar,
                "personality": bot.get_personality_display(),
            }
            for bot in chatbots
        ]
    }
    return JsonResponse(data)

@login_required
def chatbot_chat(request, pk):
    chatbot = get_object_or_404(Chatbot, pk=pk, user=request.user)
    return render(request, 'main/chatbot_chat.html', {'chatbot': chatbot})

@login_required
def ai_video_call(request):
    return render(request, 'main/ai_video_call.html')

@login_required
def get_ai_response(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        
        # Generate AI response using your existing chatbot logic
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }
        
        prompt = (
            "You are a mental health companion AI. "
            "Respond to the user in a supportive, empathetic, and helpful manner. "
            "Keep responses concise and natural, as if having a real conversation. "
            f"User: {message}\nAI:"
        )
        
        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 200,
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response_data = response.json()
            ai_reply = response_data['choices'][0]['message']['content'].strip()
            
            # Convert AI response to speech using Eleven Labs
            audio_data = text_to_speech(ai_reply)
            
            return JsonResponse({
                'reply': ai_reply,
                'audio': audio_data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def track_wellness(request):
    if request.method == 'POST':
        form = WellnessEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Wellness entry recorded successfully!')
            return redirect('dashboard')
    else:
        # Try to get today's entry
        today = timezone.now().date()
        entry = WellnessEntry.objects.filter(user=request.user, date=today).first()
        form = WellnessEntryForm(instance=entry)
    
    # Get the last 7 days of entries for the chart
    last_week = timezone.now().date() - timedelta(days=7)
    entries = WellnessEntry.objects.filter(
        user=request.user,
        date__gte=last_week
    ).order_by('date')
    
    return render(request, 'main/wellness_form.html', {
        'form': form,
        'entries': entries,
    })

@login_required
def get_wellness_data(request):
    # Get last 30 days of data
    last_month = timezone.now().date() - timedelta(days=30)
    entries = WellnessEntry.objects.filter(
        user=request.user,
        date__gte=last_month
    ).order_by('date')
    
    data = {
        'dates': [entry.date.strftime('%Y-%m-%d') for entry in entries],
        'moods': [entry.mood for entry in entries],
        'energy_levels': [entry.energy_level or 0 for entry in entries],
        'anxiety_levels': [entry.anxiety_level or 0 for entry in entries],
        'sleep_hours': [entry.sleep_hours or 0 for entry in entries],
    }
    return JsonResponse(data)

@csrf_exempt
@login_required
def save_wellness_entry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entry, created = WellnessEntry.objects.update_or_create(
                user=request.user,
                date=timezone.now().date(),
                defaults={
                    'mood': data.get('mood'),
                    'sleep_hours': data.get('sleep_hours'),
                    'energy_level': data.get('energy_level'),
                    'anxiety_level': data.get('anxiety_level'),
                    'notes': data.get('notes', '')
                }
            )
            return JsonResponse({'status': 'success', 'created': created})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def profile_settings(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    if request.method == 'POST':
        email = request.POST.get('email')
        show_adult = request.POST.get('show_adult') == 'on'
        avatar = request.FILES.get('avatar')
        if email:
            user.email = email
        if profile:
            profile.show_adult = show_adult
            if avatar:
                profile.avatar = avatar
            profile.save()
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile-settings')
    return render(request, 'main/profile_settings.html', {'user': user, 'profile': profile})
