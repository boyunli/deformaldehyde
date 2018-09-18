from django.views.generic import DetailView

from django.contrib.auth import logout
from django.views.generic import FormView, RedirectView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.http import is_safe_url
from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings

from .models import Article
from .forms import RegisterForm, LoginForm, ArticleModelForm, AccountChangeForm
from dashboard.models import SiteSettings
from comments.forms import CommentForm
from deformaldehyde.utils import get_page

class ArticleDetailView(DetailView):
    template_name = 'members/article.html'
    model = Article
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self):
        obj = super().get_object()
        obj.viewed()
        obj.image = Article.objects.get(id=int(self.kwargs[self.pk_url_kwarg])).image
        self.object = obj
        return obj

    def get_context_data(self, **kwargs):
        article_comments = self.object.comment_list()
        site_settings = SiteSettings.objects.get()

        kwargs['commentForm'] = CommentForm()
        kwargs['article_comments'] = article_comments
        kwargs['articles'] = Article.published.filter(ad_property=5)[:4]
        kwargs['sim_articles'] = Article.published.filter(category=kwargs['object'].category, ad_property=0)[:5]
        kwargs['best_articles'] = Article.published.filter(ad_property=0).order_by('-views')[:5]
        kwargs['wechat_pay_code'] = site_settings.wechat_pay_code
        kwargs['alipay_code'] = site_settings.alipay_code
        context = super().get_context_data(**kwargs)
        return context


class BackStageView(TemplateView):
    '''
    会员后台
    '''
    template_name = 'members/backstage.html'

    def get(self, request):
        user = request.user
        form = AccountChangeForm(user, initial={
            'username': user.username,
            'nickname': user.nickname,
            'mobile': user.mobile,
            'email': user.email,
            'site': user.site,
            'qq': user.qq,
            'wechat': user.wechat,
            'intro': user.intro,
            'portrait': user.portrait,
        })
        articles = user.article_set.all()
        particles, page_range = get_page(request, articles)
        context = {
            'user_change_form': form,
            'username': user.username,
            'nickname': user.nickname,
            'level': user.get_level_display,
            'email': user.email,
            'len_comments': user.comment_set.all().count(),
            'len_articles': articles.count(),
            'particles': particles,
            'page_range': page_range,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        form = AccountChangeForm(user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            url = reverse('members:member')
            return HttpResponseRedirect('{}#usertab2'.format(url))
        else:
            print(form.errors)
            return render(request, self.template_name, {'user_change_form': form})


class RegisterView(FormView):
    '''
    注册
    '''
    form_class = RegisterForm
    template_name = 'members/register.html'

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(False)
        if not user.nickname:
            user.nickname = user.username
        user.is_staff = True
        user.save(True)
        url = reverse('members:login')
        return HttpResponseRedirect(url)


class LogoutView(RedirectView):
    '''
    登出
    '''
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        from deformaldehyde.utils import cache
        cache.clear()
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        redirect_to = self.request.META.get('HTTP_REFERER', '/')
        return redirect_to


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'members/login.html'
    success_url = '/'
    redirect_field_name = 'HTTP_REFERER'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # redirect_to = self.request.GET.get(self.redirect_field_name, '/')
        redirect_to = self.request.META.get('HTTP_REFERER', '/')
        kwargs['redirect_to'] = redirect_to

        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
            from deformaldehyde.utils import cache
            if cache and cache is not None:
                cache.clear()
            print(self.redirect_field_name)
            auth.login(self.request, form.get_user())
            return super(LoginView, self).form_valid(form)
            # return HttpResponseRedirect('/')
        else:
            return self.render_to_response({
                'form': form
            })

    def get_success_url(self):
        print(self.redirect_field_name)
        # redirect_to = self.request.POST.get(self.redirect_field_name)
        redirect_to = self.request.META.get('HTTP_REFERER')
        if reverse('members:login') in redirect_to:
            redirect_to = reverse('dashboard:index')
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class ArticleEditView(TemplateView):
    template_name = 'members/article_post.html'

    def get(self, request, *args, **kwargs):
        form = ArticleModelForm()
        return render(request, self.template_name, {'article_form': form, 'form': LoginForm()})

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        form = ArticleModelForm(post, request.FILES)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            title = form_cleaned_data.get('title')
            wechat = form_cleaned_data.get('wechat')
            category = form_cleaned_data.get('category')
            tags = form_cleaned_data.get('tags')
            content = form_cleaned_data.get('content')
            image = form_cleaned_data.get('image')
            dict_ = {
                'account': request.user,
                'title': title,
                'wechat': wechat if wechat else settings.WECHAT,
                'category': category,
                'content': content,
                'image': image,
            }
            article = Article.objects.create(**dict_)
            for tag in tags:
                article.tags.add(tag)
            article.save(is_compress=True)

            return HttpResponseRedirect(reverse('members:submitted'))
        else:
            return render(request, self.template_name, {'article_form': form})

def submitted(request):
    return render(request, 'members/submitted.html')
