from django import template

register = template.Library()


@register.filter(name='persianize_digits')
def persian_digit(string):
    english_to_persian = dict(zip("0123456789", '۰۱۲۳۴۵۶۷۸۹'))
    return ''.join(english_to_persian[digit] if digit in english_to_persian else digit for digit in str(string))
