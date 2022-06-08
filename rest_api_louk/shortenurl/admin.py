from django.contrib import admin
from .models import Shortener

# Register your models here.

@admin.register(Shortener)
class ShortenerAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'created_at', 'shortener', 'updated_at' )
    search_fields = ['user__email', 'user__phone', 'shortener','url', ]
    list_filter = ('created_at', 'user',)
    class Meta:
        verbose_name = "shorten url"
        verbose_name_plural = "shorten url"
    pass