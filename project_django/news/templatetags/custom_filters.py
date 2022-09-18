from django import template


register = template.Library()


@register.filter()
def censor(text):
    for i in text.split():
        if i[0].isupper():
            text = text.replace(i, i[0] + '*' * (len(i) - 1))
    return text
