from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    # User Management
    path("accounts/", include("allauth.urls")),
    # Home
    path("", TemplateView.as_view(
        template_name="global/pages/home.html"), name='home'),
    # Users
    path("users/", include("users.urls")),
    # Projects
    path("projects/", include("projects.urls")),
    # Topics
    path("topics/", include("topics.urls")),

    # 3rd party

    # TinyMCE
    path('tinymce/', include('tinymce.urls')),
    # PWA
    path('', include('pwa.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
