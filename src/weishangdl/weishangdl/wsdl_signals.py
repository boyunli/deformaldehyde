import logging

import django.dispatch
from django.dispatch import receiver
from django.conf import settings

from weishangdl.spider_notify import SpiderNotify

logger = logging.getLogger(__name__)

article_save_signal = django.dispatch.Signal(providing_args=['id', 'is_update_views'])


@receiver(article_save_signal)
def article_save_callback(sender, **kwargs):
    id = kwargs['id']
    is_update_views = kwargs['is_update_views']
    type = sender.__name__
    obj = None
    from members.models import Article
    if type == 'Article':
        obj = Article.objects.get(id=id)
    if obj is not None:
        if not settings.TESTING and not is_update_views:
            try:
                notify_url = obj.get_full_url()
                SpiderNotify.baidu_notify([notify_url])
            except Exception as ex:
                logger.error("notify sipder", ex)
                print(ex)

