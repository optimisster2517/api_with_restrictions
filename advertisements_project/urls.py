"""
URL configuration for advertisements_project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('advertisements.urls')),
    path('', RedirectView.as_view(url='/api/advertisements/', permanent=False)),
]
