# health_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('', include('users.urls')),  # Including users' URLs
    path('health/', include('health_records.urls')),  # Include health_records URLs
    # Include other app URLs as needed
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
