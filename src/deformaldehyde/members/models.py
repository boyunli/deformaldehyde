import os
import re
import datetime
from PIL import Image as Img
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site

from ckeditor_uploader.fields import RichTextUploadingField

from dashboard.models import BaseModel, Category, Tag, AreaTag
from deformaldehyde.settings import MEDIA_URL, MEDIA_ROOT


class Account(AbstractUser):
    '''
    会员
      0、 密码保存
      1、 cookies 保存机制
      2、 如何采用邮箱验证
      3、 注册时的图片验证码机制
    '''

    MEMBER_LEVEL_CHOICES = (
        (0, '普通会员'),
        (1, '铜牌会员'),
    )

    nickname = models.CharField('昵称', max_length=100, blank=True)
    mobile = models.CharField('手机', max_length=11, blank=True)
    level = models.IntegerField(_('会员等级'), choices=MEMBER_LEVEL_CHOICES, default=0)
    portrait = models.ImageField('头像', upload_to='upload/portrait', default='upload/portrait/default.png')
    update_time = models.DateTimeField('修改时间', default=timezone.now)
    qq = models.CharField(_("QQ"), max_length=20, blank=True)
    wechat = models.CharField(_("微信"), max_length=20, blank=True)
    site = models.CharField(_("站点"), max_length=20, blank=True)
    intro = models.TextField(_("公司简介"), max_length=500, blank=True)

    # objects = BlogUserManager()

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'members_account'
        verbose_name = verbose_name_plural = '账号'


    def get_full_url(self):
        site = Site.objects.get_current().domain
        url = "https://{site}{path}".format(site=site, path=self.get_absolute_url())
        return url

    def get_portrait_url(self):
        return '{}/{}'.format(MEDIA_URL, self.portrait)

    def save(self, *args, **kwargs):
        # import pdb;pdb.set_trace()
        if self.portrait:
            img = Img.open(BytesIO(self.portrait.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((self.portrait.width/2.5, self.portrait.height/2.5), Img.ANTIALIAS)
            output= BytesIO()
            img.save(output, format='JPEG', optimize=True, quality=70)
            self.portrait= InMemoryUploadedFile(output, 'ImageField', self.portrait.name,
                                             'image/jpeg', output.getbuffer().nbytes, None)
        super(Account, self).save(*args, **kwargs)


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=2)


class Article(BaseModel):
    '''
    货源
    '''
    ROUND_CHOICES = (
        (0, '否'),
        (1, '是'),
    )
    STATUS_CHOICES = (
        (0, '待审'),
        (2, '发布'),
        (3, '拒绝'),
    )
    POSITION0 = 0
    POSITION1 = 1
    POSITION2 = 2
    POSITION3 = 3
    POSITION4 = 4
    POSITION5 = 5
    POSITION_CHOICES = (
        (POSITION0, '非广告'),
        (POSITION1, '广告A区(6)'),
        (POSITION2, '广告B区(4)'),
        (POSITION3, '广告C区(推荐-11)'),
        (POSITION4, '广告D区(5)'),
        (POSITION5, '广告E区(文章-4)'),
    )
    account = models.ForeignKey(Account, verbose_name='账号', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='标题', unique=True)
    wechat = models.CharField(_('微信'), max_length=20)
    category = models.ForeignKey(Category, verbose_name='类别', on_delete=models.CASCADE)
    content = RichTextUploadingField(_('内容'), config_name='default')
    image = models.ImageField(_('首图'),
                              help_text=(_('注：首页广告轮播图尺寸为:宽800*长300; 首页广告图片尺寸为：宽280*长210')),
                              upload_to=datetime.datetime.now().strftime('article/%Y/%m/%d'))
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    area_tags = models.ManyToManyField(AreaTag, verbose_name='地域标签', blank=True)
    views = models.PositiveIntegerField(_('阅读量'), default=0)
    status = models.IntegerField(_('状态'), choices=STATUS_CHOICES, default=0)
    ad_property = models.IntegerField(_('广告属性'), choices=POSITION_CHOICES, default=POSITION0)
    is_broadcast = models.IntegerField(_('是否广播'), choices=ROUND_CHOICES, default=0)
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-update_time']
        db_table = 'members_article'
        verbose_name = verbose_name_plural = '货源'

    def get_absolute_url(self):
        return reverse('members:article_detail', kwargs={
            'article_id': self.id,
        })

    def viewed(self):
        '''
        增加阅读数
        '''
        self.views +=1
        # update_fields 只更新数据库中的views
        self.save(update_fields=['views'], is_update_views=True)

    def comment_list(self):
        # cache_key = 'article_comments_{id}'.format(id=self.id)
        # value = cache.get(cache_key)
        # if value:
        #     logger.info('get article comments:{id}'.format(id=self.id))
        #     return value
        # else:
        comments = self.comment_set.filter(is_enable=True)
        # cache.set(cache_key, comments)
        print('set article comments:{id}'.format(id=self.id))
        return comments

    @property
    def first_para(self):
        return re.sub('[\r\s\t\n]', '', self.content[:100])

    @property
    def comment_count(self):
        return self.comment_set.all().count()

    def _resize_img(self, image, is_content=False):
        if is_content:
            image_path = os.path.join(MEDIA_ROOT, image)
        else:
            image_path = BytesIO(image.read())
        img = Img.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        if is_content:
            img.thumbnail((img.width/1.5, img.height/1.5), Img.ANTIALIAS)
            img.save(image_path, format='JPEG')
            pass
        else:
            # 除了大的轮播广告图片为800*300， 其他分类展示图片大小为 宽/长 = 280/210
            from PIL import ImageOps
            if self.ad_property == self.POSITION1:
                img = ImageOps.fit(img, (800,300), Img.ANTIALIAS)
            else:
                img = ImageOps.fit(img, (280,210), Img.ANTIALIAS)
            output= BytesIO()
            img.save(output, format='JPEG', optimize=True, quality=70)
            self.image= InMemoryUploadedFile(output, 'ImageField', image.name,
                                             'image/jpeg', output.getbuffer().nbytes, None)

    def save(self, is_compress=False, is_update_views=False, *args,  **kwargs):
        if self.image:
            # img = Img.open(BytesIO(self.image.read()))
            # if img.mode != 'RGB':
            #     img = img.convert('RGB')
            # img.thumbnail((self.image.width/1.5, self.image.height/1.5), Img.ANTIALIAS)
            # output= BytesIO()
            # img.save(output, format='JPEG', optimize=True, quality=70)
            # self.image= InMemoryUploadedFile(output, 'ImageField', self.image.name,
            #                                  'image/jpeg', output.getbuffer().nbytes, None)
            self._resize_img(self.image)
        if is_compress:
            if self.content:
                images = re.findall(r'src="(.*?)"', self.content)
                for image in images:
                    self._resize_img(image.split('/media/')[1], is_content=True)
        if self.status == 2:
           from deformaldehyde.wsdl_signals import article_save_signal
           article_save_signal.send(sender=self.__class__, is_update_views=is_update_views, id=self.id)
        super(Article, self).save(*args, **kwargs)


