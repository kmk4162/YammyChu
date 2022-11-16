from .models import Review, Restaurant, ReviewImage, RestaurantImage
from django import forms
from django.forms import ClearableFileInput

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("content", "grade")
        labels = {
            "content": "내용",
            "grade": "평점",
        }


class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ('image', )
        labels = {'image' : '이미지'}
        widgets = {'image' : ClearableFileInput(attrs={'multiple' : True}), }
        
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'lat', 'lon', 'content')
        labels = {
            'name': '이름', 'address' : '주소', 'content' : '내용'
        }
        
class RestaurantImageForm(forms.ModelForm):
    class Meta:
        model = RestaurantImage
        fields = ('image', )
        labels = {'image' : '이미지'}
        widgets = {'image' : ClearableFileInput(attrs={'multiple' : True}), }