from django.contrib import admin
from django.urls import path, include
admin.autodiscover()
from .rest_api import views, serializers
from .rest_api.views import UserList, UserDetails, GroupList, get_image, AnnotationView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
    path('annotation/save',AnnotationView.as_view()),
    path('image',get_image, name='image')
]
