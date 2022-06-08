from django.urls import include, path
from django.contrib import admin
from authapp import urls as authapp_urls
from shortenurl.views import redirect_view, create_shortener_link

app_name = 'shortenurl'
urlpatterns = [
    
    path('<str:slug>', redirect_view, name='redirect'),
    path('create_shortener/', create_shortener_link, name='create_shortener'),

]