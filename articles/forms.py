from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'category',
        ]
        labels = {
            'title' : '글 제목',
            'content' : '글 내용',
            'category' : '카테고리', 
        }