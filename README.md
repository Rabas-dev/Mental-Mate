# MentalMate

Your Personal AI Companion for Mental Wellness

MentalMate is a Django-based web application that provides personalized mental health support with AI-powered companions, mood tracking, insightful analytics, and a modern blog platform.

## Features
- AI video/voice call with ElevenLabs integration
- AI chat companions
- Wellness tracking and analytics
- Mental health blog (industry-standard UI)
- User profile and settings (with adult content toggle)
- Modern, responsive UI

## Setup
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd mentalmate
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your secrets.
5. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
6. **Create a superuser (admin):**
   ```sh
   python manage.py createsuperuser
   ```
7. **Run the server:**
   ```sh
   python manage.py runserver
   ```

## Deployment
- For Vercel or other cloud platforms, ensure you set environment variables and use a production-ready database.
- Static/media files should be served via a CDN or cloud storage in production.

## License
MIT 