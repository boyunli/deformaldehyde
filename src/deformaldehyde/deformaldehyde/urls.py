from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap

from deformaldehyde.settings import MEDIA_ROOT
from deformaldehyde.sitemap import StaticViewSitemap, ArticleSiteMap, \
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
