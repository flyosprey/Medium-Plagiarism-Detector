# Generated by Django 4.0.4 on 2022-05-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_requestdatetime_options_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='requestdata',
            name='topic_idx',
        ),
        migrations.AddIndex(
            model_name='requestdata',
            index=models.Index(fields=['topic', 'site_name'], name='topic_site_name_idx'),
        ),
    ]