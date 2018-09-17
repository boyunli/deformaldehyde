from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model,password_validation
from django.utils.translation import gettext_lazy as _
from django.forms.models import ModelChoiceField

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from dashboard.models import Category
from .models import Article

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.widgets.TextInput(attrs={'placeholder': "username", "class": "form-control"})
        self.fields['password'].widget = forms.widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.widgets.TextInput(attrs={'id': 'user_login', 'class': 'input', 'size': '30', 'tabindex': '1'})
        self.fields['email'].widget = forms.widgets.EmailInput(attrs={'id': 'user_email', 'class': 'input', 'size': '30', 'tabindex': '2', "required": "required"})
        self.fields['password1'].widget = forms.widgets.PasswordInput(
            attrs={'id':"user_pwd1", 'class':"input", 'tabindex':"3", 'size': "30"})
        self.fields['password2'].widget = forms.widgets.PasswordInput(
            attrs={'id':"user_pwd2", 'class':"input", 'tabindex':"4", 'size': "30"})

    def clean_username(self):
        '''
        不允许用户名为中文
        '''
        username = self.cleaned_data.get('username')
        import re
        pattern = re.compile(u'[\u4e00-\u9fa5]+')
        if pattern.search(username):
            raise forms.ValidationError('用户名只能包含字母，数字和仅有的@/./+/-/_符号。')
        else:
            return username

    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class AccountChangeForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': True,
        'style': 'width: 100%;',
        'id': 'user_login',
    }), required=False)
    nickname = forms.CharField(widget=forms.TextInput(attrs={
        'style': 'width: 100%;',
    }), required=False)
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'style': 'width: 100%;',
    }), required=False)
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'style': 'width: 100%;',
        'class': 'mid2',
        'readonly': True,
    }), required=False)
    site = forms.CharField(widget=forms.URLInput(attrs={
        'style': 'width: 100%;',
    }), required=False)
    qq = forms.CharField(widget=forms.TextInput(attrs={
        'style': 'width: 100%;',
    }), required=False)
    wechat = forms.CharField(widget=forms.TextInput(attrs={
        'style': 'width: 100%;',
    }), required=False)
    intro = forms.CharField(widget=forms.Textarea(attrs={
        'style': 'width: 100%;',
        'rows' : '5',
        'id': 'description',
    }), required=False)
    portrait = forms.ImageField(widget=forms.FileInput(attrs={
        'style': 'width: 100%;',
        'id': 'simple-local-avatar',
    }), required=False)
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'autofocus': True, 'id':"password",
                                          'class':"mid2",  'style': 'width: 100%;'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(attrs={'autofocus': True, 'id':"repsword",
                                          'class':"mid2",  'style': 'width: 100%;'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            return
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        """Save the new password."""
        nickname = self.cleaned_data['nickname']
        mobile = self.cleaned_data['mobile']
        site = self.cleaned_data['site']
        password = self.cleaned_data["password1"]
        qq = self.cleaned_data['qq']
        wechat = self.cleaned_data['wechat']
        intro = self.cleaned_data['intro']
        portrait = self.cleaned_data['portrait']
        if nickname:
            self.user.nickname = nickname
        if mobile:
            self.user.mobile = mobile
        if password:
            self.user.set_password(password)
        if site:
            self.user.site = site
        if qq:
            self.user.qq = qq
        if wechat:
            self.user.wechat = wechat
        if intro:
            self.user.intro = intro
        if portrait:
            self.user.portrait = portrait
        if commit:
            self.user.save()
        return self.user


class ArticleModelForm(forms.ModelForm):
    title = forms.CharField(widget= forms.TextInput(attrs={'placeholder' : '必填'}),
                            error_messages={'unique': '该信息标题重复，请更换标题！'})
    content = forms.CharField(widget=CKEditorUploadingWidget())
    category = ModelChoiceField(queryset=Category.objects.all(),
                                widget=forms.Select(attrs={'class': 'postform'}),
                                empty_label='{0} 请选择信息分类 {0}'.format('-'*26))
    wechat = forms.CharField(widget= forms.TextInput(attrs={'placeholder' : '选填'}),
                             required=False)

    class Meta:
        model = Article
        fields = ['title', 'wechat', 'category', 'area_tags', 'tags','image', 'content']
        widgets= {
            'tags': forms.SelectMultiple(attrs={'class': 'postform'}),
            'area_tags': forms.SelectMultiple(attrs={'class': 'postform'}),
        }


