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
    subject = 'Let\'s make news stories more inclusive!: Join {}'.format(PROJECT_NAME).replace(' ', '%20')
    return subject


@register.simple_tag(takes_context=False)
def invite_body(value):
    join_url = SITE_URL + '/join'
    body = 'Hi, you\'re invited to join {}. Register at <br>\
<br>\
{}<br>\
<br>\
Diverse Sources is a searchable database of underrepresented experts in the areas of science, health and the environment. Anyone who considers themselves underrepresented and is willing to respond to journalists on deadline is encouraged to join (including but not limited to appearance, ethnicity, gender expression, gender identity, language, mental health experience, nationality, physical abilities, race, religion, sex, sexual orientation, etc.).<br>\
<br>\
Let\'s make change together! Please add yourself and forward to your colleagues.<br>\
<br>\
Thank you,<br>\
Mollie Bloudoff-Indelicato<br>\
Co-Founder<br>\
<br>\
Email: DiverseSources@gmail.com<br>\
Twitter: @DiverseSources<br>\
Facebook: DiverseSources'.format(PROJECT_NAME, join_url).replace(' ', '%20').replace('<br>', '%0D%0A')
    return body

