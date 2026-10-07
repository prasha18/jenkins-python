from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Admin Panel - Technology Transfer"
admin.site.site_title = "Admin Panel - Technology Transfer"
admin.site.index_title = "Admin Panel - Technology Transfer"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tech_website.urls')),  
    path('', include('techforms.urls')),  
    path('', include('tech_repo.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)