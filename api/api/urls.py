from django.contrib import admin
from django.urls import path, include
from rest_api.views import ImageView, AnnotationView, RetrieveAnnotationView, RetrieveImageView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

schema_view = get_schema_view(
   openapi.Info(
      title="CrowdAnn API",
      default_version='v1',
      description="APIs for Crowdsourcing Platform",
    #   terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="shrivastava.4@iitj.ac.in"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('annotation/save',AnnotationView.as_view()),
    path('image',ImageView.as_view()),
    path('db/images/', RetrieveImageView.as_view()),
    path('db/annotation', RetrieveAnnotationView.as_view()),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


