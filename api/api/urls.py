from django.contrib import admin
from django.urls import path, include
from rest_api.views import get_image, annotation_save
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('annotation/save',annotation_save, name='save'),
    path('image',get_image, name='image')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)