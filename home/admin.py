from django.contrib import admin
from home.models import Plagiarism, RequestData, RequestDateTime


@admin.register(Plagiarism)
class PlagiarismConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'request_data_id', 'article_name', 'compared_article_name', 'percent_of_plagiat',
                    'article_link', 'compared_article_link')
    list_display_links = ('id',)
    search_fields = ('request_data_id',)

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(RequestDateTime)
class RequestDateTimeConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'request_data_id', 'datetime')
    list_display_links = ('id',)
    search_fields = ('id',)

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(RequestData)
class RequestDataConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'site_name', 'number_of_articles')
    list_display_links = ('id',)
    search_fields = ('topic',)

    def has_delete_permission(self, request, obj=None):
        return True

