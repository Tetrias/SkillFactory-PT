from django import template


register = template.Library()


@register.filter()
def censor(text):
    """Метод для цензурирования текста. Цензурирует только слова начинающиеся с большой буквы."""
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


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Функция для работы пагинации и фильтрации вместе."""
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
