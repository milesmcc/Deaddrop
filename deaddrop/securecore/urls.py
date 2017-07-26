from django.conf.urls import url

from . import views

app_name = "securecore"

urlpatterns = [
    url(r'^$', views.IndexView, name='index'),
    url(r'^code/$', views.CodeView, name='code'),
    url(r'^auth/code$', views.AuthCodeMethod, name='authcode'),
    url(r'^auth/sq$', views.AuthSecurityQuestionMethod, name='authsecurityquestions'),
    url(r'^auth/logout$', views.LogoutMethod, name='authlogout'),
    url(r'^securityquestions/$', views.SecurityQuestionView, name='securityquestions'),
    url(r'^drop/(?P<drop_uuid>([a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})+)/$', views.DropView, name='drop'),
    url(r'^drop/(?P<drop_uuid>([a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})+)/download$', views.DownloadDropView, name='downloaddrop'),
]
