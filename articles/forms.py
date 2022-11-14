from django import forms
from .models import Article, Comment

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

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "댓글을 남겨보세요 💬",
            }
        ),
    )
    class Meta:
        model = Comment
        fields = [
            'content',
        ]