from django.conf.urls import url
from . import views
from django.views.generic import DetailView
from .models import posts

urlpatterns = [
    url(r'^search/$', views.post, name='search'),
    url(r'^form/$', views.form, name='form'),
    url(r'^form/submit/$', views.sub, name='submit'),
    url(r'(?P<pk>\d+)/$',DetailView.as_view(model=posts,template_name='post/print.html'),name='detail')
]
