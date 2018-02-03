from django import template


register = template.Library()

@register.filter
def timezone_format(value):
	""" Check the value of the timezeone offset and, if postive, add a plus sign"""
	if value > 0:
		value = '+' + str(value)
	return value