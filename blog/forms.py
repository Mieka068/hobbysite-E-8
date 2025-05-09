# app/forms.py
from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_img']
        exclude = ['author']
        widgets = {
            'category':forms.Select(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']
