from django import template

register = template.Library()

def decim(value):
    value = str(value)
    i = len(value) - 2
    value = value[:i] + ',' + value[i:]
    return value

register.filter('decim', decim)

def hidenum(value):
    value = str(value)
    i = len(value) - 4
    value = value[i:]
    return value

register.filter('hidenum', hidenum)

def spacer(value):
    value = str(value)
    value = value.replace('_', ' ')
    value = value.capitalize()
    return value

register.filter('spacer', spacer)

def date(value):
    value = str(value)
    value = value.split(' ')[0]
    return value

register.filter('date', date)

def time(value):
    value = str(value)
    value = value.split(' ')[1]
    return value

register.filter('time', time)

def tilde(value):
    value = str(value)
    value = value.replace('e', 'é')
    return value

register.filter('tilde', tilde)

def lower(value):
    value = str(value)
    value = value.lower()
    return value

register.filter('lower', lower)

def get_index(l, i):
    return l[i]

register.filter('get_index', get_index)