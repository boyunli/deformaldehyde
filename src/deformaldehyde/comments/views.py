from .forms import CommentForm
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django import forms

from .models import Comment
from members.models import Article

class CommentPostView(FormView):
    form_class = CommentForm
    template_name = 'members/article.html'

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']

        article = Article.objects.get(pk=article_id)
        url = article.get_absolute_url()
        return HttpResponseRedirect(url + "#comments")

    def form_invalid(self, form):
        import pdb;pdb.set_trace()
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)

        if self.request.user.is_authenticated:
            form.fields.update({
                'email': forms.CharField(widget=forms.HiddenInput()),
                'name': forms.CharField(widget=forms.HiddenInput()),
            })
            user = self.request.user
            form.fields["email"].initial = user.email
            form.fields["name"].initial = user.username

        return self.render_to_response({
            'form': form,
            'article': article
        })

    def form_valid(self, form):
        """提交的数据验证合法后的逻辑"""
        user = self.request.user
        if not user.is_authenticated:
            ###  要要求先登录
            pass
        # import pdb;pdb.set_trace()

        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)
        comment = form.save(False)
        comment.article = article

        comment.account = user

        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(pk=form.cleaned_data['parent_comment_id'])
            comment.parent_comment = parent_comment

        comment.save(True)
        return HttpResponseRedirect("%s#div-comment-%d" % (article.get_absolute_url(), comment.pk))
