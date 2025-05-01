from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_on', 'updated_on', 'author']
