from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^home/$', views.diseases, name='diseases'),
    url(r'^res/$', views.res, name='res'),
    url(r'^result/$', views.res, name='res'),
    url(r'^pics/$', views.up, name='upload'),
    url(r'^upload/$', views.SaveProfile, name='uploaded'),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
