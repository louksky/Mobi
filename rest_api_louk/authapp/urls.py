from django.urls import include, path
from rest_framework import routers
from authapp import views 
from shortenurl import urls as surls
app_name = 'authapp'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('restricted/', views.restricted),
    path('shortener/', include(surls, namespace='shortener')),
]