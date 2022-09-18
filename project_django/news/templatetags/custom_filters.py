from django import template


register = template.Library()


@register.filter()
def censor(text):
    try:
        if type(text) is not str:
            raise Exception('Невозможно обработать значение, так как оно не является строкой.')
    except Exception as e:
        print(e)
    else:
        for i in text.split():
            if i[0].isupper():
                text = text.replace(i, i[0] + '*' * (len(i) - 1))
    return text
