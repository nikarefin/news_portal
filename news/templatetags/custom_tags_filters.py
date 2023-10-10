from django import template
from django.core.paginator import Paginator


register = template.Library()


@register.filter
def censor(text):
    bad_words = [
        'глаз',
        'бухгалтеров',
        'юристов',
        'рубль',
        'рубля',
    ]
    for bad_word in bad_words:
        if bad_word in text.lower():
            text = text.replace(bad_word[1:], '*'*(len(bad_word)-1))
    return text


@register.simple_tag
def get_pretty_page_range(p, number, on_each_side=1, on_ends=1):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number,
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)
