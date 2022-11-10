from .models import Review
from django import forms

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("content", "grade")
        labels = {
            "content": "내용",
            "grade": "평점",
        }