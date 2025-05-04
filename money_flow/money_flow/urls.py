from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cash_flow/', include('cash_flow.urls')),
    path('api/', include('cash_flow.api_urls')),
    path('', RedirectView.as_view(url='cash_flow/', permanent=True)),
]
