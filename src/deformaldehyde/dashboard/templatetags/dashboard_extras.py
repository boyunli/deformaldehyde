from django import template

from dashboard.models import Tag, Category, SiteSettings, AreaTag
from members.models import Article
from members.forms import LoginForm

register = template.Library()

@register.filter
def change_color(value):
    if value%2 == 0:
        return True
    else:
        return False

@register.filter
def display_humantime(value):
    return value.strftime('%m-%d')

import os
from PIL import Image
from deformaldehyde.settings import MEDIA_URL, MEDIA_ROOT
@register.filter
def thumbnail(file, size='200x200'):
    width, height = [int(x) for x in size.split('x')]
    basename, format_ = file.rsplit('.', 1)
    miniature = basename + '_' + size + '.' +  format_
    miniature_filename = os.path.join(MEDIA_ROOT, miniature.split('/media/')[1])
    miniature_url = os.path.join(MEDIA_URL, miniature)
    if not os.path.exists(miniature_filename):
        print('>>> debug: resizing the image to the format %s!' % size)
        filename = os.path.join(MEDIA_ROOT, file.split('/media/')[1])
        image = Image.open(filename)
        image.thumbnail([width, height])
        image.save(miniature_filename, image.format)
    return miniature_url

@register.inclusion_tag('dashboard/tags/login_pop.html')
def load_login_pop():
    form = LoginForm()
    return {'form': form}

@register.inclusion_tag('dashboard/tags/banner.html')
def load_banner(user):
    '''
    加载页面 顶部
    '''
    categorys = Category.objects.filter(parent=None, is_news=0)
    # import pdb;pdb.set_trace()
    return {
        'categorys': categorys,
        'user': user,
    }

@register.inclusion_tag('dashboard/tags/sidebar_tag.html')
def load_sidebar_area_tag():
    '''
    加载侧边栏 标签
    '''
    tags = AreaTag.objects.all()
    return {
        'sidebar_tags': tags,
        'name': '地域'
    }


@register.inclusion_tag('dashboard/tags/sidebar_tag.html')
def load_sidebar_tag():
    '''
    加载侧边栏 标签
    '''
    tags = Tag.objects.all()
    return {
        'sidebar_tags': tags,
        'name': '热门'
    }

@register.inclusion_tag('dashboard/tags/sidebar_new_goods.html')
def load_sidebar_flow_info():
    '''
    加载首页侧边栏 最新货源
    '''
    articles = Article.published\
        .filter(ad_property=0)[:11]
    return {
        'sidebar_flow_info': [{'id': num+1, 'url': info.get_absolute_url, 'title': info.title}
                              for num, info in enumerate(articles)],
    }

@register.inclusion_tag('dashboard/tags/sidebar_recomm.html')
def load_sidebar_recomm():
    '''
    加载首页侧边栏 本站推荐
    '''
    articles = Article.published.filter(ad_property=3)[:6]
    return {
        'recomms': articles,
    }

@register.inclusion_tag('dashboard/tags/sidebar_source_goods.html')
def load_sidebar_source_goods():
    '''
    加载首页侧边栏 热门货源
    '''
    articles = Article.published.filter(ad_property=0).order_by('-views')[:6]
    return {
        'goods': articles,
    }

@register.inclusion_tag('dashboard/tags/footer.html')
def load_footer():
    '''
    加载 footer
    '''
    from django.utils import timezone
    return {'year': timezone.now().year}

@register.inclusion_tag('dashboard/tags/scroll.html')
def load_scroll():
    '''
    加载 咨询栏
    '''
    return {
        'settings': SiteSettings.objects.get()
    }

@register.simple_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)
