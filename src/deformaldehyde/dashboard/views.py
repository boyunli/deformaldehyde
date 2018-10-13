from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Q
from itertools import chain

from .models import Category, Links, AreaTag, Tag, SiteSettings
from members.models import Article


class IndexView(TemplateView):

    def get(self, request):
        site_settings = SiteSettings.objects.get()
        ads = Article.published.filter(~Q(ad_property=0))
        categorys = Category.objects.filter(~Q(name=Category.CATEGORY6), parent__exact=None, is_news=0)
        news = Category.objects.all()

        latest_ad_left_up_round = ads.filter(ad_property=1)[:6]
        latest_ad_left_up = ads.filter(ad_property=2)[:4]

        module = categorys[:4]
        below_module = categorys[4:]

        latest_ad_left_below_round = ads.filter(ad_property=4)[:5]
        below_module = list(chain(below_module, Category.objects.filter(~Q(parent__exact=None), is_news=0)))

        ep_category = news.get(name='环保知识')
        trade_category = news.get(name='行业资讯')

        # 广播
        bd_articles = Article.published.filter(is_broadcast=1)

        context = {
            'latest_ad_left_up_round': latest_ad_left_up_round,
            'categorys': module,
            'latest_ad_left_up': latest_ad_left_up,
            'latest_ad_left_below_round': latest_ad_left_below_round,
            'latest_ad_left_below': below_module,

            'bd_articles': bd_articles,
            'ep': Article.objects.filter(category=ep_category)[:10],
            'ep_category': ep_category,
            'trade': Article.objects.filter(category=trade_category)[:10],
            'trade_category': trade_category,

            'links': Links.objects.all(),
            'head_title': site_settings.head_title,
            'head_desc': site_settings.head_desc,
            'head_keywords': site_settings.head_keywords,
        }
        return render(request, 'dashboard/index.html', context)


class ArticleListView(ListView):
    template_name = 'dashboard/article_archive.html'
    context_object_name = 'article_list'

    # 页面类型，分类目录或标签列表等
    page_type = ''

    def get_queryset(self):
        article_list = self.get_queryset_data()
        return article_list


class AreaTagView(ArticleListView):
    page_type = '地域标签归档'
    paginate_by = 20

    def get_queryset_data(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(AreaTag, slug=slug)
        tag_name = tag.name
        self.name = tag_name
        article_list = Article.published.filter(area_tags__name=tag_name)
        return article_list

    def get_context_data(self, **kwargs):
        tag_name = self.name
        kwargs['page_type'] = AreaTagView.page_type
        kwargs['tag_name'] = tag_name

        tag = AreaTag.objects.get(name=tag_name)
        kwargs['head_title'] = tag.head_title
        kwargs['head_desc'] = tag.head_desc
        kwargs['head_keywords'] = tag.head_keywords,
        return super(AreaTagView, self).get_context_data(**kwargs)


class TagDetailView(ArticleListView):
    page_type = '标签归档'
    paginate_by = 20

    def get_queryset_data(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, slug=slug)
        tag_name = tag.name
        self.name = tag_name
        article_list = Article.published.filter(tags__name=tag_name)
        return article_list

    def get_context_data(self, **kwargs):
        tag_name = self.name
        kwargs['page_type'] = TagDetailView.page_type
        kwargs['tag_name'] = tag_name

        tag = Tag.objects.get(name=tag_name)
        kwargs['head_title'] = tag.head_title
        kwargs['head_desc'] = tag.head_desc
        kwargs['head_keywords'] = tag.head_keywords,
        return super(TagDetailView, self).get_context_data(**kwargs)


class ArchiveView(ArticleListView):
    page_type = '帖文分类归档'
    paginate_by = 20

    def get_queryset_data(self):
        slug = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=slug)
        category_name = category.name
        self.name = category_name
        article_list = Article.published.filter(Q(category__name=category_name) | Q(category__parent__name=category_name))
        return article_list

    def get_context_data(self, **kwargs):
        category_name = self.name
        kwargs['page_type'] = ArchiveView.page_type
        kwargs['tag_name'] = category_name

        category = Category.objects.get(name=category_name)
        kwargs['head_title'] = category.head_title
        kwargs['head_desc'] = category.head_desc
        kwargs['head_keywords'] = category.head_keywords
        return super(ArchiveView, self).get_context_data(**kwargs)


