from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Chatbot, BlogPost
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Generate sample chatbots and blog posts for the admin user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        admin = User.objects.get(username='admin')

        # Sample data for chatbots
        chatbot_data = [
            {
                'name': 'Luna',
                'gender': 'F',
                'primary_focus': 'ANX',
                'specific_concerns': 'Specializes in helping with anxiety and panic attacks through mindfulness techniques.',
                'additional_context': 'Trained in breathing exercises and grounding techniques.',
                'personality': 'calm',
            },
            {
                'name': 'Max',
                'gender': 'M',
                'primary_focus': 'DEP',
                'specific_concerns': 'Helps with depression and mood management through positive psychology.',
                'additional_context': 'Uses CBT techniques and motivational interviewing.',
                'personality': 'motivational',
            },
            {
                'name': 'Sage',
                'gender': 'N',
                'primary_focus': 'MIN',
                'specific_concerns': 'Guides users through meditation and mindfulness practices.',
                'additional_context': 'Experienced in various meditation techniques and stress reduction.',
                'personality': 'empathetic',
            },
            {
                'name': 'Joy',
                'gender': 'F',
                'primary_focus': 'STR',
                'specific_concerns': 'Helps manage work-related stress and burnout.',
                'additional_context': 'Provides practical stress management strategies.',
                'personality': 'cheerful',
            },
        ]

        # Sample blog posts
        blog_posts = [
            {
                'title': '5 Effective Techniques for Managing Anxiety',
                'content': """Anxiety can be overwhelming, but there are proven techniques that can help you manage it effectively. Here are five strategies that you can start using today:

1. Deep Breathing Exercises
Practice deep breathing by inhaling for 4 counts, holding for 4, and exhaling for 4. This helps activate your parasympathetic nervous system.

2. Progressive Muscle Relaxation
Start from your toes and work your way up, tensing and relaxing each muscle group for 5-10 seconds.

3. Mindfulness Meditation
Take 5-10 minutes daily to focus on the present moment, acknowledging thoughts without judgment.

4. Regular Exercise
Even a 30-minute walk can help reduce anxiety symptoms by releasing endorphins.

5. Thought Journaling
Write down anxious thoughts and challenge them with rational responses.""",
                'category': 'ANX',
            },
            {
                'title': 'Understanding and Managing Depression',
                'content': """Depression is more than just feeling sad. It's a complex condition that affects millions of people worldwide. Here's what you need to know:

Key Signs of Depression:
- Persistent sadness or emptiness
- Loss of interest in activities
- Changes in sleep patterns
- Difficulty concentrating
- Physical symptoms

Management Strategies:
1. Seek Professional Help
Professional guidance is crucial for managing depression effectively.

2. Maintain Regular Routines
Structure your day with regular sleep schedules and activities.

3. Stay Connected
Maintain social connections, even when you don't feel like it.

4. Physical Activity
Regular exercise can be as effective as medication for mild depression.

5. Self-Care Practices
Focus on basic needs: eating well, sleeping enough, and personal hygiene.""",
                'category': 'DEP',
            },
            {
                'title': 'The Power of Mindfulness in Daily Life',
                'content': """Mindfulness isn't just a buzzword - it's a powerful tool for mental well-being. Here's how to incorporate it into your daily routine:

1. Morning Mindfulness
Start your day with 5 minutes of mindful breathing before checking your phone.

2. Mindful Eating
Focus on the taste, texture, and smell of your food during meals.

3. Walking Meditation
Practice awareness of your surroundings during daily walks.

4. Body Scan Practice
Take regular breaks to check in with your body and release tension.

5. Mindful Communication
Listen actively and respond thoughtfully in conversations.

Remember: Mindfulness is a skill that improves with practice.""",
                'category': 'MIN',
            },
            {
                'title': 'Building Healthy Sleep Habits',
                'content': """Quality sleep is fundamental to mental health. Here are essential tips for better sleep:

1. Consistent Schedule
Go to bed and wake up at the same time daily, even on weekends.

2. Create a Sleep-Friendly Environment
- Keep your bedroom cool and dark
- Use comfortable bedding
- Minimize noise disruptions

3. Evening Routine
Develop a calming routine to signal your body it's time to sleep:
- Dim lights an hour before bed
- Avoid screens
- Try light stretching or reading

4. Diet Considerations
- Avoid caffeine after 2 PM
- Don't eat heavy meals close to bedtime
- Limit alcohol consumption

5. Managing Sleep Anxiety
If you can't sleep, don't stay in bed tossing and turning. Get up and do a calming activity until you feel sleepy.""",
                'category': 'SLE',
            },
        ]

        # Create chatbots
        for data in chatbot_data:
            Chatbot.objects.create(user=admin, **data)
            self.stdout.write(self.style.SUCCESS(f'Created chatbot: {data["name"]}'))

        # Create blog posts
        for post in blog_posts:
            BlogPost.objects.create(author=admin, **post)
            self.stdout.write(self.style.SUCCESS(f'Created blog post: {post["title"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated sample data'))