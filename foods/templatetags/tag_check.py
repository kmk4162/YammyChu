from django import template

register = template.Library()

@register.filter
def tag_check(review):
    content = review.content
    tags = review.tags.all()
    for tag in tags:
        content = content.replace(tag.content, f'<a href="#">{tag.content}</a>')
    return content