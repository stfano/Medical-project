# Generated by Django 5.0.2 on 2024-03-03 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0006_chatbot_username_userinteractionlog_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatbot',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userinteractionlog',
            name='user',
        ),
    ]
