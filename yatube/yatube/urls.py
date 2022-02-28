from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
]
