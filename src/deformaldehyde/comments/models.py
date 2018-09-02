from django.db import models

from django.conf import settings
from django.utils.timezone import now

from members.models import Article


class Comment(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name="上级评论", blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField('正文', max_length=500)
    is_enable = models.BooleanField('是否显示', default=True, blank=False, null=False)
    create_time = models.DateTimeField('创建时间', default=now)
    update_time = models.DateTimeField('更新时间', default=now)

    class Meta:
        ordering = ['-create_time']
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'create_time'

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
