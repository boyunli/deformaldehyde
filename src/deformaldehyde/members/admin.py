from django.contrib import admin
from django.utils.html import format_html

from .models import Account, Article

admin.site.site_header = '甲醛克星网'
admin.site.site_title = '甲醛克星网'

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    exclude = ('slug', 'create_time', 'update_time')
    search_fields = ('nickname',)
    list_display = ('id', 'nickname', 'password', 'mobile', 'level')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 针对列表页
    search_fields = ('account__nickname' , 'title')
    list_display = ('account', 'title', 'category', 'status',
                    'ad_property', 'preview')
    list_editable = ['ad_property', 'category', 'status']
    list_filter = ('status', 'ad_property', 'category', 'update_time', 'is_broadcast', 'account__nickname')
    list_per_page = 20
    date_hierarchy = 'update_time'

    # 针对详情编辑页
    exclude = ('slug', 'create_time', 'update_time', 'views')
    fieldsets = (
        ('base info', {'fields': ['account', 'title',
                                  'wechat', 'category',
                                  'ad_image', 'image',
                                  'is_broadcast',
                                  'status', 'ad_property']}),
        ("Content", {'fields':['content', 'tags', 'area_tags']})
    )
    filter_horizontal=('tags', 'area_tags')

    def preview(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>',
                               obj.get_absolute_url(), obj.pk)
    preview.short_description = '预览'

    def get_queryset(self, request):
        """
        使当前登录的用户只能看到自己发的贴
        """
        qs = super(ArticleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=Account.objects.filter(user_name=request.user))




