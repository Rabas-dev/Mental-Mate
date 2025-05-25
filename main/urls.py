from django.urls import path
from . import views
from .views import character_chat, chatbot_list_json

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Wellness Tracking URLs
    path('wellness/track/', views.track_wellness, name='track-wellness'),
    path('wellness/data/', views.get_wellness_data, name='wellness-data'),
    path('wellness/save/', views.save_wellness_entry, name='save-wellness'),
    
    # Existing URLs
    # Chatbot URLs
    path('chatbots/', views.ChatbotListView.as_view(), name='chatbot-list'),
    path('chatbots/create/', views.ChatbotCreateView.as_view(), name='chatbot-create'),
    path('chatbots/<int:pk>/update/', views.ChatbotUpdateView.as_view(), name='chatbot-update'),
    path('chatbots/<int:pk>/delete/', views.ChatbotDeleteView.as_view(), name='chatbot-delete'),
    path('chatbots/<int:pk>/chat/', views.chatbot_chat, name='chatbot-chat'),
    
    # Blog URLs
    path('blog/', views.BlogPostListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog-delete'),
    path('signup/', views.signup, name='signup'),
    path('character-chat/', character_chat, name='character_chat'),
    path('chatbot-list-json/', chatbot_list_json, name='chatbot_list_json'),
    
    # Video Call URLs
    path('ai-video-call/', views.ai_video_call, name='ai_video_call'),
    path('get-ai-response/', views.get_ai_response, name='get_ai_response'),
    path('profile/settings/', views.profile_settings, name='profile-settings'),
]