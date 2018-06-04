from django import template
from sourcelist.settings import EMAIL_HOST_USER, PROJECT_NAME, SITE_URL


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
def convert_special_characters_to_html_entities(value):
    """ encode special characters HTML encoding to make it a little harder to scrape """
    CONVERSION_MAPPING = [
        ('@', '&#64;'),
        ('.', '&#46;'),
        ('_', '&#95;'),
        ('-', '&#45;'),
        ('(', '&#40;'),
        (')', '&#41;'),
        ('+', '&#43;'),
    ]
    try:
        for code in CONVERSION_MAPPING:
            value = value.replace(code[0], code[1])
    except:
        pass
    return value


@register.simple_tag(takes_context=False)
def invite_bcc(value):
    return EMAIL_HOST_USER


@register.simple_tag(takes_context=False)
def invite_subject(value):
    subject = 'You\'re invited to join Diverse Sources'.replace(' ', '%20')
    return subject


@register.simple_tag(takes_context=False)
def invite_body(value):
    body = 'Hi, you\'re invited to join {}. Register at {}'.format(PROJECT_NAME, SITE_URL).replace(' ', '%20')
    return body

