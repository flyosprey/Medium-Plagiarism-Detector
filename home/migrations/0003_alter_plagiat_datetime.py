# Generated by Django 4.0.4 on 2022-05-01 16:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_plagiat_datetime_alter_plagiat_plagiat_article_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plagiat',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]