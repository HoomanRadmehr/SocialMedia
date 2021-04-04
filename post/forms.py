from django import forms
from .models import Post
from comment.models import Comment
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']


class DeletePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class AddReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

