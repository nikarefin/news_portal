from django import template


register = template.Library()


@register.filter()
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
