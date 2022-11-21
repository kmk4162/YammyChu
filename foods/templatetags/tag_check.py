from django import template
from articles.models import Team

register = template.Library()

@register.filter
def tag_check(review):
    content = review.content
    if review.store_name == None:
        team = Team.objects.get(pk=review.restaurant_name.team.pk)
    else:
        team = Team.objects.get(pk=review.store_name.team.pk)
    tags = review.tags.all()
    for tag in tags:
        content = content.replace(tag.content, '<a class="text-decoration-none" href="/foods/{}/{}/tag/">{}</a>'.format(team.pk, tag.pk, tag.content))
    return content