from django import template


register = template.Library()

@register.filter
def timezone_format(value):
    """ Check the value of the timezeone offset and, if postive, add a plus sign"""
    try:
        if int(value) > 0:
            value = '+' + str(value)
    except:
        value = ''
    return value


@register.filter
def reformat_email(value):
    """ encode special characters HTML encoding to make it a little harder to scrape """
    try:
        value = value.replace('@', '&#64;')
    except:
        pass
    try:
        value = value.replace('.', '&#46;')
    except:
        pass
    try:
        value = value.replace('_', '&#95;')
    except:
        pass
    return value
