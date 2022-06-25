from django.db import models
from django.utils import timezone


class RequestData(models.Model):
    id = models.AutoField(primary_key=True)
    site_name = models.CharField(max_length=200, null=False, blank=False)
    topic = models.CharField(max_length=200, null=False, blank=False)
    number_of_articles = models.PositiveIntegerField(null=False, blank=False, default=100)

    class Meta:
        indexes = [
            models.Index(fields=['topic', "site_name"], name='topic_site_name_idx'),
        ]


class RequestDateTime(models.Model):
    id = models.AutoField(primary_key=True)
    request_data = models.ForeignKey(RequestData, on_delete=models.CASCADE, default=None)
    datetime = models.DateTimeField(null=False, blank=False, editable=False, default=timezone.now)

    class Meta:
        verbose_name = 'Plagiarism'
        indexes = [
            models.Index(fields=['datetime'], name='datetime_idx'),
        ]


class Plagiarism(models.Model):
    id = models.AutoField(primary_key=True)
    request_data = models.ForeignKey(RequestData, on_delete=models.CASCADE, default=None)
    article_name = models.CharField(max_length=200, null=False, blank=False)
    compared_article_name = models.CharField(max_length=200, null=False, blank=False, default="")
    article_text = models.CharField(max_length=1500, null=False, blank=False, default="")
    compared_article_text = models.CharField(max_length=1500, null=False, blank=False, default="")
    article_link = models.URLField(null=False, blank=False)
    compared_article_link = models.URLField(null=False, blank=False, default="")
    percent_of_plagiat = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        verbose_name = 'Plagiarism'
        indexes = [
            models.Index(fields=['percent_of_plagiat'], name='percent_of_plagiat_idx'),
        ]
