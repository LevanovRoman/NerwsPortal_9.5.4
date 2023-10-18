from django import template
from string import punctuation

register = template.Library()

bad_words2 = ['редиска', 'чувак', 'ихний', 'евонный', 'экскалатор']


@register.filter()
def bad_words(text_string):
    res = []
    try:
        for word in text_string.split():
            if word.lower().strip(punctuation) in bad_words2:
                if word[-1] in punctuation:
                    word = word[0] + '*' * (len(word) - 2) + word[-1]
                else:
                    word = word[0] + '*' * (len(word) - 1)
            res.append(word)
    except Exception:
        print("Oops! That was no string. Try again...")
    return ' '.join(res)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
