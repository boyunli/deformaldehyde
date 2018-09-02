from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

def get_page(request, items, display_amount=15,
            after_range_num=5, bevor_range_num=4):
    paginator = Paginator(items, display_amount)
    try:
        page = int(request.GET.get('page', 1))
        print('\033[92m get_page: %s:\033[0m' % page)
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    except (InvalidPage, PageNotAnInteger):
        items = paginator.page(1)
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:page+bevor_range_num]
    return items, page_range


