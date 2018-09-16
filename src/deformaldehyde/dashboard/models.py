from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from uuslug import slugify


class BaseModel(models.Model):
    slug = models.SlugField(default='no-slug', max_length=160, blank=True)
    create_time = models.DateTimeField(_('创建时间'), default=timezone.now)
    update_time = models.DateTimeField(_('更新时间'), default=timezone.now)

    def get_full_url(self):
        site = Site.objects.get_current().domain
        url = "https://{site}{path}".format(site=site, path=self.get_absolute_url())
        return url

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == 'no-slug' or not self.id:
            slug = self.title if 'title' in self.__dict__ else self.name
            self.slug = slugify(slug)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(BaseModel):
    '''
    首页主要板块: 根据货源类别
    '''
    NEWS_CHOICES = (
        (0, '否'),
        (1, '是'),
    )
    CATEGORY1 = '甲醛的危害'
    CATEGORY2 = '除甲醛百科'
    CATEGORY3 = '除甲醛产品'
    CATEGORY4 = '除甲醛公司'
    CATEGORY5 = '除甲醛加盟'
    CATEGORY6 = '除甲醛案例'
    CATEGORY61 = '家装除甲醛'
    CATEGORY62 = '汽车除甲醛'
    CATEGORY63 = '工程除甲醛'
    CATEGORY7 = '环保知识'
    CATEGORY8 = '行业资讯'

    CATEGORY_CHOICES = (
        (CATEGORY1, CATEGORY1),
        (CATEGORY2, CATEGORY2),
        (CATEGORY3, CATEGORY3),
        (CATEGORY4, CATEGORY4),
        (CATEGORY5, CATEGORY5),
        (CATEGORY6, CATEGORY6),
        (CATEGORY61, CATEGORY61),
        (CATEGORY62, CATEGORY62),
        (CATEGORY63, CATEGORY63),
        (CATEGORY7, CATEGORY7),
        (CATEGORY8, CATEGORY8),
    )
    name = models.CharField(_('商品类别'), choices=CATEGORY_CHOICES, default=CATEGORY2,
                                max_length=20, unique=True)
    parent  = models. ForeignKey ('self', null=True , blank=True, on_delete=models.CASCADE, related_name='children')
    sequence = models.IntegerField(_('排序'), unique=True, help_text=_('数字从小到大排列分类位置.'))
    head_title = models.TextField(_('HeadTitle'), blank=False)
    head_desc = models.TextField(_('HeadDesc'), blank=False)
    head_keywords = models.TextField(_('HeadKeywords'), blank=False)
    is_news = models.IntegerField(_('IsNews'), default=0, choices=NEWS_CHOICES)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['sequence']
        db_table = 'dashboard_category'
        verbose_name = verbose_name_plural = _('栏目分类')

    def get_published_articles(self):
        '''
        后续优化时： 这个方法可以缓存起来
        '''
        return self.article_set.filter(status=2, ad_property=0)

    def get_absolute_url(self):
        return reverse('dashboard:article_category', kwargs={'category_name': self.slug})


class Links(BaseModel):
    '''
    友情链接
    '''
    name = models.CharField(_('站点'), max_length=15)
    url = models.URLField(_('URL'), max_length=300)
    sequence = models.IntegerField(_('排序'), unique=True, help_text=_('数字从小到大排列标签位置.'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['sequence']
        db_table = 'dashboard_links'
        verbose_name = verbose_name_plural = _('友情链接')


class AreaTag(BaseModel):
    '''
    地域标签
    '''
    name = models.CharField('标签名', max_length=30, unique=True)
    head_title = models.TextField(_('HeadTitle'), blank=False)
    head_desc = models.TextField(_('HeadDesc'), blank=False)
    head_keywords = models.TextField(_('HeadKeywords'), blank=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:area_tag', kwargs={'tag_name': self.slug})

    # @cache_decorator(60 * 60 * 10)
    # def get_article_count(self):
    #     return Article.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        db_table = 'dashboard_area_tag'
        verbose_name = "地域标签"
        verbose_name_plural = verbose_name


class Tag(BaseModel):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, unique=True)
    head_title = models.TextField(_('HeadTitle'), blank=False)
    head_desc = models.TextField(_('HeadDesc'), blank=False)
    head_keywords = models.TextField(_('HeadKeywords'), blank=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:tag_detail', kwargs={'tag_name': self.slug})

    # @cache_decorator(60 * 60 * 10)
    # def get_article_count(self):
    #     return Article.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        db_table = 'dashboard_tag'
        verbose_name = "热门标签"
        verbose_name_plural = verbose_name


class SiteSettings(models.Model):
    '''
    站点设置
    '''
    sitename = models.CharField("网站名称", max_length=100, null=False, blank=False, default='')
    head_title = models.TextField("首页标题", max_length=1000, null=False, blank=False, default='')
    head_desc = models.TextField("首页描述", max_length=1000, null=False, blank=False, default='')
    head_keywords = models.TextField("首页关键字", max_length=1000, null=False, blank=False, default='')
    article_sub_length = models.IntegerField("文章摘要长度", default=300)
    sidebar_flow_info_count = models.IntegerField("侧边栏信息流数目", default=10)
    sidebar_recomm_count = models.IntegerField("侧边栏推荐帖文数目", default=5)

    qq_bar_code = models.ImageField(_('QQ二维码'), upload_to='site/qq')
    qq = models.CharField(_("QQ"), max_length=20)

    wechat_pay_code = models.ImageField(_('微信支付维码'), upload_to='site/wechat')
    alipay_code = models.ImageField(_('支付宝二维码'), upload_to='site/alipay')
    phone = models.CharField('手机', max_length=11)

    beiancode = models.CharField('备案号', max_length=2000, null=True, blank=True, default='')
    analyticscode = models.TextField("网站统计代码", max_length=1000, null=False, blank=False, default='')
    show_gongan_code = models.BooleanField('是否显示公安备案号', default=False, null=False)
    gongan_beiancode = models.TextField('公安备案号', max_length=2000, null=True, blank=True, default='')

    class Meta:
        db_table = 'dashboard_settings'
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sitename

    def clean(self):
        if SiteSettings.objects.exclude(id=self.id).count():
            raise ValidationError(_('只能有一个配置'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from deformaldehyde.utils import cache
        cache.clear()
