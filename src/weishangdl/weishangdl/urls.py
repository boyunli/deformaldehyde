"""weishangdl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap

from weishangdl.settings import MEDIA_ROOT
from weishangdl.sitemap import StaticViewSitemap, ArticleSiteMap, \
    CategorySiteMap, TagSiteMap

sitemaps = {
    'static': StaticViewSitemap,
    'articles': ArticleSiteMap,
    'Category': CategorySiteMap,
    'Tag': TagSiteMap
}


urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'', include('dashboard.urls', namespace='dashboard')),
    url('', include('members.urls', namespace='members')),
    url('', include('comments.urls', namespace='comments')),
    url(r'^search/', include('haystack.urls')),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]

from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
