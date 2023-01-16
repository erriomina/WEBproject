from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from WedDeveloperApp import views

urlpatterns = [
    path("", views.index),
    path("demand/", views.demand),
    path("geography/", views.geography),
    path("skills/", views.skills),
    path("last_vacancies/", views.last_vacancies)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)