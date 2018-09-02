from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from .forms import LoginForm

app_name = 'members'
urlpatterns = [

    path(r'article/<int:article_id>.html',
         views.ArticleDetailView.as_view(), name='article_detail'),
    url(r'^login/$', views.LoginView.as_view(success_url='/'), name='login', kwargs={'authentication_form': LoginForm}),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^member/$', login_required(views.BackStageView.as_view(), login_url='/'), name='member'),
    path(r'post', views.ArticleEditView.as_view(), name='article_post'),
    path(r'submitted', views.submitted, name='submitted'),
]

