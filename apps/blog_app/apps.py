from django.apps import AppConfig


class BlogAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog_app'
    verbose_name = 'بخش مقالات'
