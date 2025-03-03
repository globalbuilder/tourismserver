from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth endpoints (from SimpleJWT)
    path('api/auth/', include('accounts.auth_urls')), 

    # Our apps
    path('api/accounts/', include('accounts.urls')),
    path('api/attractions/', include('attractions.urls')),
    path('api/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
