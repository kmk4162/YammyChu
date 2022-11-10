from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Article(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    category_choices = (
        ('잡담'),
        ('질문'),
        ('야구'),
        ('음식'),
        ('직관모집'),
        ('기타'),
    )
    category = models.CharField(max_length=5, choices=category_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(default=0)
    user_article_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_articles")

    @property
    def update_hits(self):
        self.hits = self.hits + 1
        self.save()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Stadium(models.Model):
    name_choices = (
        ('인천 SSG 랜더스필드'),
        ('고척 스카이돔'),
        ('서울종합운동장 야구장'),
        ('수원 케이티 위즈 파크'),
        ('광주-기아 챔피언스 필드'),
        ('창원 NC 파크'),
        ('대구 삼성 라이온즈 파크'),
        ('사직 야구장'),
        ('서울종합운동장 야구장'),
        ('대전 한화생명 이글스파크'),
    )
    name = models.CharField(max_length=15)
    address_choices = (
        ('인천광역시 미추홀구 매소홀로 618'),
        ('서울특별시 구로구 경인로 430'),
        ('서울특별시 송파구 잠실동 올림픽로 25'),
        ('경기도 수원시 장안구 경수대로 893'),
        ('광주광역시 북구 서림로 10'),
        ('경상남도 창원시 마산회원구 삼호로 63'),
        ('대구광역시 수성구 야구전설로 1'),
        ('부산광역시 동래구 사직로 45'),
        ('서울특별시 송파구 잠실동 올림픽로 25'),
        ('대전광역시 중구 대종로 373'),
    )
    address = models.TextField(choices=address_choices)

class Team(models.Model):
    name_choices = (
        ('SSG 랜더스'),
        ('키움 히어로즈'),
        ('LG 트윈스'),
        ('kt wiz'),
        ('KIA 타이거즈'),
        ('NC 다이노스'),
        ('삼성 라이온즈'),
        ('롯데 자이언츠'),
        ('두산 베어스'),
        ('한화 이글스'),
    )
    name = models.CharField(max_length=10, choices=name_choices)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    color_choices = (
        ('#CE0E2D', 'SSG 랜더스'),
        ('#820024', '키움 히어로즈'),
        ('#C30452', 'LG 트윈스'),
        ('#000000', 'kt wiz'),
        ('#EA0029', 'KIA 타이거즈'),
        ('#315288', 'NC 다이노스'),
        ('#074CA1', '삼성 라이온즈'),
        ('#002955', '롯데 자이언츠'),
        ('#131230', '두산 베어스'),
        ('#FF6600', '한화 이글스'),
    )
    color = models.ColorField(choices=color_choices)
    logo = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(800, 800)],
        format="JPEG",
        options={"quality": 100},
    )
