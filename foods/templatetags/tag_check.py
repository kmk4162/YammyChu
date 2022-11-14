from django import template

register = template.Library()

@register.filter
def tag_check(review):
    content = review.content
    team = review.name.team
    tags = review.tags.all()
    for tag in tags:
        content = content.replace(tag.content, '<a class="text-decoration-none" href="/foods/home/{}/{}/tag">{}</a>'.format(team.pk, tag.pk, tag.content))
    return content