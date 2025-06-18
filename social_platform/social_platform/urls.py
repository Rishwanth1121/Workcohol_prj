from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('social.urls')),         # Homepage and main app
    path('admin/', admin.site.urls),          # Admin panel
    path('chat/', include('chat.urls')),      # Chat routes (under /chat/)
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
