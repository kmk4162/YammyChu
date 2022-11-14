from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator
from articles.models import Team

class Store(models.Model):
    name = models.TextField(max_length=30)
    lat = models.TextField()
    lon = models.TextField()    
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(1200, 960)],
        format="JPEG",
        options={"quality": 80},
        null=True
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_stores', default=1)
    items = models.TextField()
    detail = models.TextField()
    
class Tag(models.Model):
    content = models.TextField(unique=True)
    
class Review(models.Model):
    tags = models.ManyToManyField('Tag', related_name='tag_articles', blank=True)
    name = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_reviews')
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_image')
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})