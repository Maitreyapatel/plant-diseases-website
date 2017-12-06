from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^signup/$',views.signuppage,name='signup'),
    url(r'^register/$',views.UserFormView,name='register'),
    url(r'^login/$',views.loginpage,name='login'),
    url(r'^log/$',views.login,name='log'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^profile/$',views.profile,name='profile'),
    #url(r'^$',ListView.as_view(queryset=Post.objects.all().order_by("-date"),template_name="blog/blog.html"))
]
