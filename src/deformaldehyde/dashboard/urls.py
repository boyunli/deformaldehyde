from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(r'tag/<slug:tag_name>.html', views.TagDetailView.as_view(), name='tag_detail'),
    path(r'area/<slug:tag_name>.html', views.AreaTagView.as_view(), name='area_tag'),
    path(r'category/<slug:category_name>.html', views.ArchiveView.as_view(), name='article_category'),
]
