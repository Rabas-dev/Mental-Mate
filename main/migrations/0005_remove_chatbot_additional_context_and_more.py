# Generated by Django 5.1.7 on 2025-05-25 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_wellnessentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatbot',
            name='additional_context',
        ),
        migrations.AlterField(
            model_name='chatbot',
            name='personality',
            field=models.CharField(choices=[('empathetic', 'Empathetic Listener'), ('motivational', 'Motivational Coach'), ('calm', 'Calm Supporter'), ('cheerful', 'Cheerful Friend'), ('practical', 'Practical Advisor'), ('just_like_her', 'Just Like Her'), ('just_like_him', 'Just Like Him')], default='empathetic', max_length=255),
        ),
        migrations.AlterField(
            model_name='chatbot',
            name='primary_focus',
            field=models.CharField(choices=[('ANX', 'Anxiety'), ('DEP', 'Depression'), ('STR', 'Stress'), ('REL', 'Relationships'), ('SLE', 'Sleep'), ('MIN', 'Mindfulness'), ('GEN', 'General Support'), ('PATCHUP', 'Patchup')], max_length=255),
        ),
        migrations.AlterField(
            model_name='chatbot',
            name='specific_concerns',
            field=models.TextField(blank=True),
        ),
    ]
