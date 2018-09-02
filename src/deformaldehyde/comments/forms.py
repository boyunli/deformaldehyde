from .models import Comment
from django import forms
from django.forms import ModelForm


class CommentForm(ModelForm):
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': "4",  'tabindex': '1','name': 'comment', 'id': 'comment'})
        }
