# Generated by Django 4.0.4 on 2022-05-31 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_plagiat_datetime_remove_plagiat_topic_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Plagiat',
            new_name='Plagiarism',
        ),
    ]
